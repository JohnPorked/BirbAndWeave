extends Area2D

@onready var playerhitbox = $Playerhitbox

func _on_body_entered(body) -> void:
	# Ensure the body is the player
	if body.name == "Playuh":
		var player = body
		
		# Check if player is dashing - skip damage if they are
		if player.has_method("is_dashing") and player.is_dashing():
			print("Player dodged the hit by dashing!")
			return
		
		print("You've been hit")
		var anim_sprite = player.get_node("AnimatedSprite2D")
		
		if anim_sprite:
			anim_sprite.play("Hit")  # Play the "Hit" animation
			Engine.time_scale = 0.01
			await get_tree().create_timer(0.03).timeout
			Engine.time_scale = 1
			anim_sprite.play("idle")
			
			# Optional: Reduce player health
			if player.has_method("take_damage"):
				player.take_damage(1)
