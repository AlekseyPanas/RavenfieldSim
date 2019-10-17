class Layer:
    def __init__(self, visual_prevent, update_prevent, event_prevent):
        # Activated if this layer is being prevented by another layer
        self.visual_lock = False
        # Prevents all previous layers from being drawn
        self.visual_prevent = visual_prevent

        # Prevents all previous layers from visually updating
        self.update_prevent = update_prevent
        # Activated if this layer is being prevented by another layer
        self.update_lock = False

        # Activated if this layer is being prevented by another layer
        self.event_lock = False
        # Events are disabled for all previous layers if False
        self.event_prevent = True if self.visual_prevent or self.update_prevent else event_prevent

    def run_layer(self, screen):
        pass
