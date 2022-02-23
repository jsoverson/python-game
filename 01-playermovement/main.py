import arcade
from arcade.pymunk_physics_engine import PymunkPhysicsEngine

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 1
TILE_SCALING = 1
SPRITE_PIXEL_SIZE = 96

LAYER_NAME_PLAYER = "Player"

# Constants used to track if the player is facing left or right
DOWN_FACING = 0
LEFT_FACING = 1
RIGHT_FACING = 2
UP_FACING = 3

# How fast to move, and how fast to run the animation
PLAYER_MOVE_FORCE = 4000 * CHARACTER_SCALING
UPDATES_PER_FRAME = 10


class PlayerCharacter(arcade.Sprite):
    def __init__(self):
        super().__init__()

        # Default to face-right
        self.character_face_direction = RIGHT_FACING

        # Used for flipping between image sequences
        self.cur_texture = 0
        self.scale = CHARACTER_SCALING
        self.force = (0, 0)

        # --- Load Textures ---
        main_path = "../assets/tilesets/heroes/2x/Character sprites/Beastmaster"

        # Load textures for idle standing
        self.idle_textures = arcade.load_spritesheet(
            f"{main_path}_idle.png", SPRITE_PIXEL_SIZE, SPRITE_PIXEL_SIZE, 4, 16)

        # Load textures for walking
        self.walk_textures = arcade.load_spritesheet(
            f"{main_path}_walk.png", SPRITE_PIXEL_SIZE, SPRITE_PIXEL_SIZE, 4, 16)

        self.texture = self.idle_textures[0]

    def update_animation(self, delta_time: float = 1 / 60):
        # Figure out if we need to flip face left or right
        if self.force[0] < 0:
            self.character_face_direction = LEFT_FACING
        elif self.force[0] > 0:
            self.character_face_direction = RIGHT_FACING
        elif self.force[1] > 0:
            self.character_face_direction = UP_FACING
        else:
            self.character_face_direction = DOWN_FACING

        self.cur_texture += 1
        if self.cur_texture > 3 * UPDATES_PER_FRAME:
            self.cur_texture = 0
        frame = self.cur_texture // UPDATES_PER_FRAME

        direction = self.character_face_direction

        # Idle animation
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_textures[(direction)*4+frame]
            return

        # Walking animation
        self.texture = self.walk_textures[(direction)*4+frame]


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(fullscreen=True)

        self.scene = None

        self.player_sprite = None

        # Our physics engine
        self.physics_engine = None

        self.up_pressed = False
        self.down_pressed = False
        self.right_pressed = False
        self.left_pressed = False

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        self.scene = arcade.Scene()

        self.player_sprite = PlayerCharacter()
        self.player_sprite.center_x = SPRITE_PIXEL_SIZE / 2
        self.player_sprite.center_y = SPRITE_PIXEL_SIZE / 2
        self.scene.add_sprite(LAYER_NAME_PLAYER, self.player_sprite)

        damping = 1
        gravity = (0, 0)

        self.physics_engine = PymunkPhysicsEngine(damping=damping,
                                                  gravity=gravity)

        self.physics_engine.add_sprite(self.player_sprite,
                                       friction=.9,
                                       moment_of_inertia=PymunkPhysicsEngine.MOMENT_INF,
                                       damping=0.000001,
                                       collision_type="player",
                                       max_velocity=400)

    def on_draw(self):
        """Render the screen."""

        # Clear the screen to the background color
        self.clear()
        self.scene.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.up_pressed = True
        if key == arcade.key.DOWN:
            self.down_pressed = True
        if key == arcade.key.LEFT:
            self.left_pressed = True
        if key == arcade.key.RIGHT:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP:
            self.up_pressed = False
        if key == arcade.key.DOWN:
            self.down_pressed = False
        if key == arcade.key.LEFT:
            self.left_pressed = False
        if key == arcade.key.RIGHT:
            self.right_pressed = False

    def on_update(self, delta_time):
        """Movement and game logic"""

        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        vert_force = 0
        hori_force = 0

        if self.up_pressed and not self.down_pressed:
            vert_force = PLAYER_MOVE_FORCE
        elif self.down_pressed and not self.up_pressed:
            vert_force = -PLAYER_MOVE_FORCE
        if self.left_pressed and not self.right_pressed:
            hori_force = -PLAYER_MOVE_FORCE
        elif self.right_pressed and not self.left_pressed:
            hori_force = PLAYER_MOVE_FORCE

        force = (hori_force, vert_force)

        self.player_sprite.force = force
        self.physics_engine.apply_force(
            self.player_sprite, self.player_sprite.force)

        self.scene.update_animation(
            delta_time, [LAYER_NAME_PLAYER]
        )

        self.physics_engine.step()


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
