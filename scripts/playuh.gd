extends CharacterBody2D

const SPEED = 225.0
const DASH_SPEED = 700.0
const DASH_DURATION = 0.2
const DASH_COOLDOWN = 1.0

var health = 1
var can_dash = true
var dashing = false  # Renamed from is_dashing
var dash_timer = 0.0
var dash_cooldown_timer = 0.0
var dash_direction = Vector2.ZERO

# Optional dash effect
@onready var dash_particles = $DashParticles if has_node("DashParticles") else null
@onready var dash_ghost_timer = 0.0
const GHOST_SPAWN_TIME = 0.03

func _physics_process(delta: float) -> void:
	# Handle dash cooldown
	if dash_cooldown_timer > 0:
		dash_cooldown_timer -= delta
		if dash_cooldown_timer <= 0:
			can_dash = true
	
	# Get movement input
	var direction = Vector2.ZERO
	direction.x = Input.get_axis("ui_left", "ui_right")
	direction.y = Input.get_axis("ui_up", "ui_down")
	
	if direction != Vector2.ZERO:
		direction = direction.normalized()  # Normalize to prevent diagonal speed boost
	
	# Handle dash activation
	if Input.is_action_just_pressed("Shift") and can_dash and direction != Vector2.ZERO:
		# Start dash
		dashing = true
		can_dash = false
		dash_timer = DASH_DURATION
		dash_cooldown_timer = DASH_COOLDOWN
		dash_direction = direction
		
		# Optional: Play dash effect
		if dash_particles:
			dash_particles.emitting = true
	
	# Handle dash movement
	if dashing:
		velocity = dash_direction * DASH_SPEED
		dash_timer -= delta
		
		# Optional: Create dash ghost effect
		dash_ghost_timer -= delta
		if dash_ghost_timer <= 0:
			spawn_dash_ghost()
			dash_ghost_timer = GHOST_SPAWN_TIME
		
		if dash_timer <= 0:
			dashing = false
			if dash_particles:
				dash_particles.emitting = false
	else:
		# Normal movement
		velocity = direction * SPEED
	
	move_and_slide()

# Check if player is currently dashing (used for invulnerability check)
func is_dashing() -> bool:
	return dashing

# Optional: Method for enemies to damage the player
func take_damage(amount: int) -> void:
	if dashing:
		return  # No damage during dash
	
	health -= amount
	if health <= 0:
		die()

# Optional: Handle player death
func die() -> void:
	# Implement death behavior
	print("Player died")
	# You could trigger game over screen, respawn, etc.

# Optional dash afterimages are disabled until a DashGhost scene is added.
func spawn_dash_ghost() -> void:
	pass