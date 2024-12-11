import tkinter as tk  # Importing the Tkinter module for GUI creation
import random  # Importing the random module to generate random numbers

# Function to start or reset the game
def start_game():
    global ball_y, ball_velocity, pipes, score, game_over  # Declare global variables to track game state
    ball_y = canvas_height // 2  # Initialize the ball's vertical position at the center of the canvas
    ball_velocity = 0  # Reset the ball's velocity to 0
    pipes = [[canvas_width, random.randint(pipe_gap, canvas_height - pipe_gap)]]  # Create the initial pipe
    score = 0  # Reset the score to 0
    game_over = False  # Reset the game over state
    canvas.itemconfig(ball, fill="yellow")  # Reset the ball's color to yellow
    update_game()  # Start updating the game

# Function to update the game state (ball position, pipes, collisions, etc.)
def update_game():
    global ball_y, ball_velocity, pipes, score, game_over  # Use global variables to track changes

    if game_over:  # If the game is over, stop updating
        return

    # Update ball position
    ball_velocity += gravity  # Apply gravity to the ball's velocity
    ball_y += ball_velocity  # Update the ball's position based on velocity

    # Update pipe positions
    for pipe in pipes:
        pipe[0] -= pipe_speed  # Move each pipe to the left

    # Remove pipes that have moved off-screen
    pipes = [pipe for pipe in pipes if pipe[0] > -pipe_width]

    # Add new pipes as needed
    if pipes and pipes[-1][0] < canvas_width - pipe_spacing:
        pipes.append([canvas_width, random.randint(pipe_gap, canvas_height - pipe_gap)])  # Add a new pipe

    # Check for collisions
    for pipe_x, pipe_y in pipes:
        # Check if the ball hits a pipe or goes out of bounds
        if (pipe_x < ball_x + ball_width // 2 < pipe_x + pipe_width and 
            (ball_y - ball_height // 2 < pipe_y - pipe_gap // 2 or ball_y + ball_height // 2 > pipe_y + pipe_gap // 2)) or \
            ball_y > canvas_height or ball_y < 0:
            game_over = True  # Set game over state
            canvas.itemconfig(ball, fill="red")  # Change ball's color to red
            score_label.config(text=f"Game Over! Score: {score}")  # Display game over message
            return

    # Update score when the ball successfully passes a pipe
    for pipe in pipes:
        if pipe[0] == ball_x:  # Check if the pipe has passed the ball's x position
            score += 1

    # Redraw the ball
    canvas.coords(ball, ball_x - ball_width // 2, ball_y - ball_height // 2, 
                  ball_x + ball_width // 2, ball_y + ball_height // 2)

    # Redraw pipes
    canvas.delete("pipe")  # Remove existing pipe graphics
    for pipe_x, pipe_y in pipes:
        canvas.create_rectangle(pipe_x, 0, pipe_x + pipe_width, pipe_y - pipe_gap // 2, fill="green", tags="pipe")  # Top pipe
        canvas.create_rectangle(pipe_x, pipe_y + pipe_gap // 2, pipe_x + pipe_width, canvas_height, fill="green", tags="pipe")  # Bottom pipe

    # Update the score label
    score_label.config(text=f"Score: {score}")

    # Schedule the next frame
    root.after(30, update_game)  # Call update_game again after 30 milliseconds

# Function to make the ball bounce upwards
def bounce():
    global ball_velocity  # Use global variable for ball's velocity
    if not game_over:  # If the game is not over
        ball_velocity = -bounce_strength  # Set velocity to a negative value for upward movement

# Initialize the main application window
root = tk.Tk()
root.title("THE SKYBALL")  # Set the title of the window

# Bind the space bar to make the ball bounce
root.bind("<space>", lambda event: bounce())

# Game variables
canvas_width = 800  # Width of the game canvas
canvas_height = 400  # Height of the game canvas
ball_x = canvas_width // 4  # Horizontal position of the ball
ball_width = 30  # Width of the ball
ball_height = 30  # Height of the ball
ball_y = canvas_height // 2  # Initial vertical position of the ball
ball_velocity = 0  # Initial velocity of the ball
pipes = [[canvas_width, random.randint(100, canvas_height - 100)]]  # List to store pipe positions
pipe_width = 50  # Width of each pipe
pipe_gap = 120  # Gap between the top and bottom parts of the pipe
pipe_spacing = 300  # Horizontal distance between consecutive pipes
pipe_speed = 5  # Speed at which the pipes move to the left
game_over = False  # Game over state
gravity = 2  # Downward force applied to the ball
bounce_strength = 12  # Upward force applied when the ball bounces
score = 0  # Initial score

# Create the canvas where the game will be displayed
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="skyblue")
canvas.pack()

# Draw the ball on the canvas
ball = canvas.create_oval(ball_x - ball_width // 2, ball_y - ball_height // 2, 
                          ball_x + ball_width // 2, ball_y + ball_height // 2, fill="yellow")

# Add a label to display the score
score_label = tk.Label(root, text="Score: 0", font=("Arial", 14))
score_label.pack()

# Add buttons for bouncing and resetting the game
bounce_button = tk.Button(root, text="Bounce", command=bounce, font=("Arial", 12))
bounce_button.pack()
reset_button = tk.Button(root, text="Reset Game", command=start_game, font=("Arial", 12))
reset_button.pack()

# Start the game
start_game()

# Start the Tkinter main loop
root.mainloop()  # Run the GUI application
