class GameObject:
    """
    Basic game object capable of executing named actionables such as Openable and Examinable.

    Attributes:
        id (str): Unique identifier for the game object.
        actionables (dict): Dictionary mapping action names to actionable objects.

    Methods:
        get_id(): Returns the unique ID of the game object.
        execute_actionable(name, *params): Executes the specified actionable if available.
        has_actionable(name): Checks if the given actionable is available.
    """

    def __init__(self, obj_id, obj_name, actionables=None):
        self.id = obj_id
        self.name = obj_name
        self.actionables = actionables or {}

    def get_id(self):
        """Return the unique ID of the game object."""
        return self.id

    def execute_actionable(self, name, *params):
        """
        Execute the named actionable if it exists and has an exec method.

        Args:
            name (str): Name of the actionable to execute.
            *params: Parameters to pass to the actionable's exec method.

        Returns:
            Any: The return value of the actionable's exec method, if called.
        """
        actionable = self.actionables.get(name)
        if actionable and callable(getattr(actionable, "exec", None)):
            return actionable.exec(*params)

    def get_actionable(self, name):
        """
        Retrieve an actionable object by its name.
        Args:
            name (str): The name of the actionable.

        Returns:
            The actionable object if found, else None.
        """
        return self.actionables.get(name)

    def has_actionable(self, name):
        """
        Check if the game object has the specified actionable.

        Args:
            name (str): Name of the actionable.

        Returns:
            bool: True if the actionable exists, False otherwise.
        """
        return name in self.actionables
