#!/usr/bin/env python3
"""
Branch Summary Generator for Clockify Tasks

This script generates a concise summary of commits from a specific branch
that can be easily copied into a Clockify task description.
"""

import argparse
import subprocess
import sys
from datetime import datetime, timedelta
from typing import List, Tuple


class BranchSummaryGenerator:
    def __init__(self, branch_name: str, days_back: int = 7, branch_only: bool = False):
        self.branch_name = branch_name
        self.days_back = days_back
        self.branch_only = branch_only
        self.since_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
        
    def run_command(self, cmd: List[str]) -> Tuple[str, int]:
        """Run a shell command and return output and exit code."""
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            return result.stdout.strip(), result.returncode
        except Exception as e:
            print(f"Error running command {' '.join(cmd)}: {e}", file=sys.stderr)
            return "", 1
    
    def get_main_branch(self) -> str:
        """Try to determine the main branch (main, master, develop, etc.)."""
        # Common main branch names to check
        main_branches = ['main', 'master', 'develop', 'dev']
        
        for branch in main_branches:
            # Check if branch exists remotely
            cmd = ["git", "show-ref", "--verify", "--quiet", f"refs/remotes/origin/{branch}"]
            _, exit_code = self.run_command(cmd)
            if exit_code == 0:
                return branch
        
        # If no common main branch found, try to get the default branch from remote
        cmd = ["git", "symbolic-ref", "refs/remotes/origin/HEAD"]
        output, exit_code = self.run_command(cmd)
        if exit_code == 0 and output:
            return output.replace('refs/remotes/origin/', '')
        
        return ""

    def get_branch_commits(self) -> List[dict]:
        """Get commits from the specified branch."""
        cmd = [
            "git", "--no-pager", "log",
            f"--since={self.since_date}",
            "--pretty=format:%H|%an|%ad|%s",
            "--date=short"
        ]
        
        if self.branch_only:
            # Get commits only from this branch (exclude merges from other branches)
            # This shows commits that were made directly on this branch
            main_branch = self.get_main_branch()
            if main_branch and main_branch != self.branch_name:
                cmd.append(f"{main_branch}..{self.branch_name}")
            else:
                # If we can't determine main branch or we ARE on main, show all commits but exclude merge commits
                cmd.extend(["--no-merges", self.branch_name])
        else:
            cmd.append(self.branch_name)
        
        output, exit_code = self.run_command(cmd)
        if exit_code != 0:
            print(f"Error getting commits for branch '{self.branch_name}': {output}", file=sys.stderr)
            return []
        
        commits = []
        for line in output.split('\n'):
            if line.strip():
                parts = line.split('|', 3)
                if len(parts) == 4:
                    commit_hash, author, date, message = parts
                    commits.append({
                        "hash": commit_hash[:8],  # Short hash
                        "author": author,
                        "date": date,
                        "message": message.strip()
                    })
        
        return commits

    def get_pr_info(self) -> dict:
        """Get PR information if this branch has an associated PR."""
        # First, try to find PR with this branch as head
        cmd = ["gh", "pr", "list", "--head", self.branch_name, "--json", "number,title,url,state"]
        output, exit_code = self.run_command(cmd)
        
        if exit_code == 0 and output.strip():
            try:
                import json
                pr_data = json.loads(output)
                if pr_data:
                    return pr_data[0]  # Return first (should be only) PR
            except (json.JSONDecodeError, ImportError):
                pass
        
        # If no direct PR found, try to search for PRs that might contain this branch's commits
        # This is helpful when the branch has been merged and deleted
        cmd = ["gh", "pr", "list", "--state", "all", "--limit", "20", "--json", "number,title,url,state,headRefName"]
        output, exit_code = self.run_command(cmd)
        
        if exit_code == 0 and output.strip():
            try:
                import json
                pr_data = json.loads(output)
                for pr in pr_data:
                    if pr.get('headRefName') == self.branch_name:
                        return pr
            except (json.JSONDecodeError, ImportError):
                pass
        
        return None

    def categorize_commit_message(self, message: str) -> str:
        """Categorize a commit message."""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['feat:', 'feature:', 'add ']):
            return "✨ Feature"
        elif any(word in message_lower for word in ['fix:', 'bug:', 'resolve']):
            return "🐛 Fix"
        elif any(word in message_lower for word in ['refactor:', 'refact:']):
            return "♻️ Refactor"
        elif any(word in message_lower for word in ['test:', 'tests:']):
            return "🧪 Test"
        elif any(word in message_lower for word in ['doc:', 'docs:']):
            return "📚 Docs"
        elif any(word in message_lower for word in ['chore:', 'cleanup']):
            return "🧹 Chore"
        elif any(word in message_lower for word in ['hotfix:', 'urgent']):
            return "🚨 Hotfix"
        else:
            return "📦 Other"

    def generate_summary(self) -> str:
        """Generate the branch summary for Clockify."""
        commits = self.get_branch_commits()
        pr_info = self.get_pr_info()
        
        if not commits:
            return f"No commits found in branch '{self.branch_name}' in the last {self.days_back} days."
        
        # Branch info
        summary = f"# Branch: {self.branch_name}\n\n"
        
        # PR info if available
        if pr_info:
            status_emoji = "✅" if pr_info['state'] == 'MERGED' else "🔄" if pr_info['state'] == 'OPEN' else "❌"
            summary += f"**Pull Request**: {status_emoji} PR #{pr_info['number']} - {pr_info['title']}\n"
            summary += f"**PR URL**: {pr_info['url']}\n\n"
        else:
            # Try to find PR by searching in commit messages for PR numbers
            pr_numbers = set()
            for commit in commits:
                # Look for "Merge pull request #123" or "(#123)" patterns
                import re
                pr_matches = re.findall(r'#(\d+)', commit['message'])
                pr_numbers.update(pr_matches)
            
            if pr_numbers:
                summary += f"**Related PRs**: #{', #'.join(sorted(pr_numbers, key=int))}\n\n"
        
        # Summary stats
        summary += f"**Period**: Last {self.days_back} days (since {self.since_date})\n"
        summary += f"**Total Commits**: {len(commits)}\n"
        
        # Contributors
        authors = list(set(commit['author'] for commit in commits))
        if len(authors) == 1:
            summary += f"**Developer**: {authors[0]}\n\n"
        else:
            summary += f"**Developers**: {', '.join(authors)}\n\n"
        
        # Categorize commits
        categories = {}
        for commit in commits:
            category = self.categorize_commit_message(commit['message'])
            if category not in categories:
                categories[category] = []
            categories[category].append(commit)
        
        # Work summary by category
        summary += "## Work Summary:\n\n"
        for category, category_commits in categories.items():
            summary += f"### {category} ({len(category_commits)} commits)\n"
            for commit in category_commits:
                # Clean up commit message
                clean_message = commit['message']
                if ':' in clean_message and any(prefix in clean_message.lower() for prefix in ['feat:', 'fix:', 'refactor:', 'test:', 'doc:', 'chore:']):
                    clean_message = clean_message.split(':', 1)[1].strip()
                
                summary += f"- {clean_message} `{commit['hash']}`\n"
            summary += "\n"
        
        # Recent commits chronological list
        if len(commits) <= 10:
            summary += "## Commit History:\n\n"
            for commit in commits:
                category_emoji = self.categorize_commit_message(commit['message']).split()[0]
                summary += f"- {category_emoji} **{commit['date']}**: {commit['message']} `{commit['hash']}`\n"
        
        return summary

def main():
    parser = argparse.ArgumentParser(description='Generate branch summary for Clockify task')
    parser.add_argument('branch', nargs='?', help='Branch name (current branch if not specified)')
    parser.add_argument('--days', '-d', type=int, default=7, 
                       help='Number of days to look back (default: 7)')
    parser.add_argument('--file', '-f', type=str, 
                       help='Output file path (optional, prints to stdout if not specified)')
    parser.add_argument('--compact', '-c', action='store_true',
                       help='Generate compact summary suitable for task descriptions')
    parser.add_argument('--branch-only', '-b', action='store_true',
                       help='Show only commits made directly on this branch (exclude merged commits)')
    
    args = parser.parse_args()
    
    # Get current branch if not specified
    if not args.branch:
        result = subprocess.run(["git", "branch", "--show-current"], 
                              capture_output=True, text=True, check=False)
        if result.returncode == 0:
            args.branch = result.stdout.strip()
        else:
            print("Error: Could not determine current branch. Please specify branch name.", file=sys.stderr)
            sys.exit(1)
    
    print(f"📝 Generating summary for branch: {args.branch}")
    
    generator = BranchSummaryGenerator(args.branch, args.days, args.branch_only)
    summary = generator.generate_summary()
    
    if args.compact:
        # Generate a more compact version for task descriptions
        # Get the PR info directly from the generator instead of parsing
        pr_info = generator.get_pr_info()
        lines = summary.split('\n')
        compact_lines = []
        in_work_summary = False
        
        for line in lines:
            if line.startswith('## Work Summary:'):
                in_work_summary = True
                continue
            elif line.startswith('## Commit History:'):
                break
            elif in_work_summary and line.strip():
                if line.startswith('### '):
                    # Category header
                    compact_lines.append(f"\n**{line[4:]}**")
                elif line.startswith('- '):
                    # Commit item
                    compact_lines.append(line)
        
        # Build compact summary with PR info
        compact_summary = f"Branch: {args.branch}\n"
        
        # Add PR information if available
        if pr_info:
            status_emoji = "✅" if pr_info['state'] == 'MERGED' else "🔄" if pr_info['state'] == 'OPEN' else "❌"
            compact_summary += f"\n**Pull Request**: {status_emoji} PR #{pr_info['number']} - {pr_info['title']}\n"
        else:
            # Try to find PR numbers from commit messages
            import re
            pr_numbers = set()
            for line in lines:
                if line.startswith('- '):
                    pr_matches = re.findall(r'#(\d+)', line)
                    pr_numbers.update(pr_matches)
            
            if pr_numbers:
                compact_summary += f"\n**Related PRs**: #{', #'.join(sorted(pr_numbers, key=int))}\n"
        
        compact_summary += '\n'.join(compact_lines)
        summary = compact_summary
    
    if args.file:
        with open(args.file, 'w') as f:
            f.write(summary)
        print(f"✅ Summary saved to {args.file}")
    else:
        print("\n" + "="*60)
        print(summary)
        print("="*60)
    
    print(f"✅ Summary generated for branch '{args.branch}'")

if __name__ == "__main__":
    main()