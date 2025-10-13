import pytest

from src.core.base import FluentBase


class TestFluentBase:
    """Test suite for FluentBase class."""

    def test_stage_with_lambda(self):
        """Test stage method with a lambda function."""
        fluent = FluentBase()
        fluent.test_value = None

        result = fluent.stage("Setting value", lambda f: setattr(f, "test_value", 42))

        assert fluent.test_value == 42
        assert result is fluent  # Verify fluent chaining

    def test_stage_with_method_name(self):
        """Test stage method with a string method name."""

        class TestFluent(FluentBase):
            def __init__(self):
                super().__init__()
                self.value = 0

            def set_value(self, val):
                self.value = val

        fluent = TestFluent()
        result = fluent.stage("Setting value", "set_value", 100)

        assert fluent.value == 100
        assert result is fluent  # Verify fluent chaining

    def test_stage_with_kwargs(self):
        """Test stage method with keyword arguments."""

        class TestFluent(FluentBase):
            def __init__(self):
                super().__init__()
                self.data = {}

            def update_data(self, key, value):
                self.data[key] = value

        fluent = TestFluent()
        result = fluent.stage("Updating data", "update_data", "name", value="test")

        assert fluent.data == {"name": "test"}
        assert result is fluent

    def test_stage_with_custom_spinner(self):
        """Test stage method with custom spinner."""
        fluent = FluentBase()
        fluent.test_value = None

        # Should not raise an error with custom spinner
        result = fluent.stage(
            "Processing", lambda f: setattr(f, "test_value", "done"), spinner="point"
        )

        assert fluent.test_value == "done"
        assert result is fluent

    def test_stage_chaining(self):
        """Test multiple stage calls can be chained."""

        class TestFluent(FluentBase):
            def __init__(self):
                super().__init__()
                self.steps = []

            def add_step(self, step):
                self.steps.append(step)

        fluent = TestFluent()
        result = (
            fluent.stage("Step 1", "add_step", "first")
            .stage("Step 2", "add_step", "second")
            .stage("Step 3", lambda f: f.add_step("third"))
        )

        assert fluent.steps == ["first", "second", "third"]
        assert result is fluent

    def test_stage_with_nonexistent_method(self):
        """Test stage raises AttributeError for nonexistent method."""
        fluent = FluentBase()

        with pytest.raises(AttributeError):
            fluent.stage("Calling invalid", "nonexistent_method")
