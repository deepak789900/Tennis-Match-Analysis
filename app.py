from flask import Flask, jsonify, render_template, send_file
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as ticker



import io

app = Flask(__name__)

# Load player statistics
player_stats_path = "output\\player_stats.json"
player_stats_df = pd.read_json(player_stats_path, orient="records")


@app.route("/")
def index():
    return render_template("index.html")  # Frontend dashboard


@app.route("/api/player-stats")
def get_player_stats():
    """API to fetch player statistics"""
    stats = player_stats_df.to_dict(orient="records")
    return jsonify(stats)


@app.route("/api/highest-shot-speed")
def get_highest_shot_speed():
    """
    API to fetch the data for both players with the highest shot speed.
    """
    player_1_row = player_stats_df.loc[player_stats_df["player_1_average_shot_speed"].idxmax()]
    player_2_row = player_stats_df.loc[player_stats_df["player_2_average_shot_speed"].idxmax()]

    player_1_data = {
        "frame_num": player_1_row["frame_num"],
        "average_player_speed": player_1_row["player_1_average_player_speed"],
        "average_shot_speed": player_1_row["player_1_average_shot_speed"]
    }

    player_2_data = {
        "frame_num": player_2_row["frame_num"],
        "average_player_speed": player_2_row["player_2_average_player_speed"],
        "average_shot_speed": player_2_row["player_2_average_shot_speed"]
    }

    return jsonify({
        "player_1_data": player_1_data,
        "player_2_data": player_2_data
    })


@app.route("/api/select-best-player")
def select_best_player():
    """
    API to select the best player based on criteria
    and return the frame with the highest shot speed.
    """
    criteria = "average_shot_speed"  # Default criteria for selection
    player_1_avg = player_stats_df["player_1_average_shot_speed"].mean()
    player_2_avg = player_stats_df["player_2_average_shot_speed"].mean()
    best_player = "Player 1" if player_1_avg > player_2_avg else "Player 2"

    player_1_row = player_stats_df.loc[player_stats_df["player_1_average_shot_speed"].idxmax()]
    player_2_row = player_stats_df.loc[player_stats_df["player_2_average_shot_speed"].idxmax()]

    return jsonify({
        "best_player": best_player,
        "criteria": criteria,
        "player_1_data": {
            "frame_num": player_1_row["frame_num"],
            "average_player_speed": player_1_row["player_1_average_player_speed"],
            "average_shot_speed": player_1_row["player_1_average_shot_speed"]
        },
        "player_2_data": {
            "frame_num": player_2_row["frame_num"],
            "average_player_speed": player_2_row["player_2_average_player_speed"],
            "average_shot_speed": player_2_row["player_2_average_shot_speed"]
        }
    })


@app.route("/api/player-averages", methods=["GET"])
def get_player_averages():
    """
    API to calculate and return the average speeds and shot speeds
    for Player 1 and Player 2.
    """
    player_1_avg_speed = player_stats_df["player_1_average_player_speed"].mean()
    player_1_avg_shot_speed = player_stats_df["player_1_average_shot_speed"].mean()
    player_2_avg_speed = player_stats_df["player_2_average_player_speed"].mean()
    player_2_avg_shot_speed = player_stats_df["player_2_average_shot_speed"].mean()

    return jsonify({
        "player_1_average_speed": player_1_avg_speed,
        "player_1_average_shot_speed": player_1_avg_shot_speed,
        "player_2_average_speed": player_2_avg_speed,
        "player_2_average_shot_speed": player_2_avg_shot_speed
    })


@app.route("/api/best-player-by-shot-speed")
def get_best_player_by_shot_speed():
    """
    API to return the best player based on average shot speed.
    """
    player_1_avg_shot_speed = player_stats_df["player_1_average_shot_speed"].mean()
    player_2_avg_shot_speed = player_stats_df["player_2_average_shot_speed"].mean()

    best_player = "Player 1" if player_1_avg_shot_speed > player_2_avg_shot_speed else "Player 2"

    return jsonify({
        "best_player": best_player,
        "player_1_avg_shot_speed": player_1_avg_shot_speed,
        "player_2_avg_shot_speed": player_2_avg_shot_speed
    })


@app.route("/api/best-player-max-speeds")
def get_best_player_max_speeds():
    """
    API to fetch the maximum player speed and maximum shot speed for the best player.
    """
    player_1_avg_shot_speed = player_stats_df["player_1_average_shot_speed"].mean()
    player_2_avg_shot_speed = player_stats_df["player_2_average_shot_speed"].mean()

    if player_1_avg_shot_speed > player_2_avg_shot_speed:
        best_player = "Player 1"
        max_player_speed = player_stats_df["player_1_average_player_speed"].max()
        max_shot_speed = player_stats_df["player_1_average_shot_speed"].max()
    else:
        best_player = "Player 2"
        max_player_speed = player_stats_df["player_2_average_player_speed"].max()
        max_shot_speed = player_stats_df["player_2_average_shot_speed"].max()

    return jsonify({
        "best_player": best_player,
        "max_player_speed": max_player_speed,
        "max_shot_speed": max_shot_speed
    })


@app.route("/api/player-comparison-graph")
def get_player_comparison_graph():
    """
    API to generate and return the player speed comparison graph.
    """
    try:
        # Ensure required columns are present
        required_columns = {"frame_num", "player_1_average_player_speed", "player_2_average_player_speed"}
        if not required_columns.issubset(player_stats_df.columns):
            return {"error": "Data is missing required columns."}, 400

        # Apply Seaborn style
        sns.set_theme(style="whitegrid")

        # Create a styled graph
        fig, ax = plt.subplots(figsize=(12, 7))  # Larger size for better visuals

        # Plot data with custom styles
        player_stats_df.plot(
            x="frame_num",
            y=["player_1_average_player_speed", "player_2_average_player_speed"],
            ax=ax,
            linewidth=2.5,
            color=["#007ACC", "#FF5733"],  # Distinct, colorblind-friendly colors
            alpha=0.9  # Slight transparency
        )

        # Add titles and labels with enhanced styling
        ax.set_title("Player Speed Comparison Over Time", fontsize=18, fontweight="bold", color="#333333")
        ax.set_xlabel("Frame Number", fontsize=15, labelpad=10)
        ax.set_ylabel("Average Speed (units/s)", fontsize=15, labelpad=10)

        # Customize tick parameters
        ax.tick_params(axis="x", labelsize=12, rotation=30)
        ax.tick_params(axis="y", labelsize=12)

        # Add a grid with custom style
        ax.grid(visible=True, linestyle="--", linewidth=0.6, alpha=0.8)

        # Annotate max values
        player1_max = player_stats_df["player_1_average_player_speed"].max()
        player2_max = player_stats_df["player_2_average_player_speed"].max()
        player1_frame = player_stats_df.loc[player_stats_df["player_1_average_player_speed"].idxmax(), "frame_num"]
        player2_frame = player_stats_df.loc[player_stats_df["player_2_average_player_speed"].idxmax(), "frame_num"]

        ax.annotate(
            f"Max: {player1_max:.2f}",
            xy=(player1_frame, player1_max),
            xytext=(player1_frame + 10, player1_max + 0.5),
            arrowprops=dict(facecolor="#007ACC", arrowstyle="->", lw=1.5),
            fontsize=12,
            color="#007ACC",
        )
        ax.annotate(
            f"Max: {player2_max:.2f}",
            xy=(player2_frame, player2_max),
            xytext=(player2_frame + 10, player2_max + 0.5),
            arrowprops=dict(facecolor="#FF5733", arrowstyle="->", lw=1.5),
            fontsize=12,
            color="#FF5733",
        )

        # Format the legend
        ax.legend(
            ["Player 1 Speed", "Player 2 Speed"],
            fontsize=13,
            loc="upper left",
            frameon=True,
            facecolor="white",
            shadow=True,
        )

        # Automatically adjust y-axis limits for better visualization
        ax.set_ylim(0, max(player1_max, player2_max) + 1)

        # Tighten layout
        plt.tight_layout()

        # Save the figure to a BytesIO object
        img = io.BytesIO()
        plt.savefig(img, format="png", dpi=300)  # High resolution
        img.seek(0)
        plt.close(fig)  # Prevent memory leaks

        return send_file(img, mimetype="image1/png")

    except Exception as e:
        return {"error": str(e)}, 500

@app.route("/api/player-shot-speed-bar")
def player_shot_speed_bar():
    """
    API to generate and return a bar graph comparing shot speed data of players.
    """
    try:
        # Compute average shot speeds
        player_1_avg_shot_speed = player_stats_df["player_1_average_shot_speed"].mean()
        player_2_avg_shot_speed = player_stats_df["player_2_average_shot_speed"].mean()

        # Create a DataFrame for visualization
        shot_speed_data = pd.DataFrame({
            "Player": ["Player 1", "Player 2"],
            "Average Shot Speed": [player_1_avg_shot_speed, player_2_avg_shot_speed]
        })

        # Set style
        sns.set_theme(style="whitegrid")

        # Create figure and axis
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.barplot(x="Player", y="Average Shot Speed", data=shot_speed_data, ax=ax, palette=["#007ACC", "#FF5733"])
        
        # Add labels and title
        ax.set_title("Comparison of Players' Average Shot Speed", fontsize=14, fontweight="bold")
        ax.set_ylabel("Shot Speed (units/s)", fontsize=12)
        ax.set_xlabel("Player", fontsize=12)
        
        # Display values on bars
        for p in ax.patches:
            ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2, p.get_height()),
                        ha='center', va='bottom', fontsize=12, fontweight='bold', color='black')
        
        plt.tight_layout()

        # Save plot to BytesIO
        img = io.BytesIO()
        plt.savefig(img, format='png', dpi=300)
        img.seek(0)
        plt.close(fig)

        return send_file(img, mimetype='image/png')

    except Exception as e:
        return jsonify({"error": str(e)}), 500






@app.route("/api/player-performance-feedback")
def get_player_performance_feedback():
    """
    API to provide feedback to players based on their performance.
    """
    try:
        # Calculate overall averages
        player_1_avg_speed = player_stats_df["player_1_average_player_speed"].mean()
        player_1_avg_shot_speed = player_stats_df["player_1_average_shot_speed"].mean()
        player_2_avg_speed = player_stats_df["player_2_average_player_speed"].mean()
        player_2_avg_shot_speed = player_stats_df["player_2_average_shot_speed"].mean()

        # Calculate standard deviations (to measure consistency)
        player_1_speed_std = player_stats_df["player_1_average_player_speed"].std()
        player_1_shot_std = player_stats_df["player_1_average_shot_speed"].std()
        player_2_speed_std = player_stats_df["player_2_average_player_speed"].std()
        player_2_shot_std = player_stats_df["player_2_average_shot_speed"].std()

        # Generate feedback for each player
        player_1_feedback = []
        if player_1_avg_speed < player_2_avg_speed:
            player_1_feedback.append(
                "Improve your overall movement speed to match or exceed Player 2's pace."
            )
        if player_1_avg_shot_speed < player_2_avg_shot_speed:
            player_1_feedback.append(
                "Focus on increasing shot speed to challenge your opponent more effectively."
            )
        if player_1_speed_std > 2:
            player_1_feedback.append(
                "Work on maintaining a consistent speed throughout the match."
            )
        if player_1_shot_std > 2:
            player_1_feedback.append(
                "Ensure your shots are consistent to avoid losing momentum during key moments."
            )

        player_2_feedback = []
        if player_2_avg_speed < player_1_avg_speed:
            player_2_feedback.append(
                "Improve your overall movement speed to match or exceed Player 1's pace."
            )
        if player_2_avg_shot_speed < player_1_avg_shot_speed:
            player_2_feedback.append(
                "Focus on increasing shot speed to challenge your opponent more effectively."
            )
        if player_2_speed_std > 2:
            player_2_feedback.append(
                "Work on maintaining a consistent speed throughout the match."
            )
        if player_2_shot_std > 2:
            player_2_feedback.append(
                "Ensure your shots are consistent to avoid losing momentum during key moments."
            )

        # Compile the feedback into a JSON response
        return jsonify({
            "player_1_feedback": player_1_feedback,
            "player_2_feedback": player_2_feedback,
            "player_1_stats": {
                "average_speed": player_1_avg_speed,
                "average_shot_speed": player_1_avg_shot_speed,
                "speed_consistency": player_1_speed_std,
                "shot_consistency": player_1_shot_std
            },
            "player_2_stats": {
                "average_speed": player_2_avg_speed,
                "average_shot_speed": player_2_avg_shot_speed,
                "speed_consistency": player_2_speed_std,
                "shot_consistency": player_2_shot_std
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/shot_speed_over_time")
def shot_speed_over_time():
    plt.figure(figsize=(12, 5))
    sns.lineplot(x=player_stats_df["frame_num"], y=player_stats_df["player_1_last_shot_speed"], label="Player 1 Shot Speed", marker="o")
    sns.lineplot(x=player_stats_df["frame_num"], y=player_stats_df["player_2_last_shot_speed"], label="Player 2 Shot Speed", marker="o")
    plt.xlabel("Frame Number")
    plt.ylabel("Shot Speed")
    plt.title("Shot Speed Over Time")
    plt.legend()
    plt.grid()
    img = io.BytesIO()
    plt.savefig(img, format="png", dpi=300)
    img.seek(0)
    plt.close()
    return send_file(img, mimetype="image/png")

@app.route("/api/shot_speed_vs_player_speed")
def shot_speed_vs_player_speed():
    plt.figure(figsize=(8, 5))
    sns.scatterplot(x=player_stats_df["player_1_last_shot_speed"], y=player_stats_df["player_1_last_player_speed"], label="Player 1", alpha=0.7)
    sns.scatterplot(x=player_stats_df["player_2_last_shot_speed"], y=player_stats_df["player_2_last_player_speed"], label="Player 2", alpha=0.7)
    plt.xlabel("Shot Speed")
    plt.ylabel("Player Speed")
    plt.title("Shot Speed vs Player Speed")
    plt.legend()
    plt.grid()
    img = io.BytesIO()
    plt.savefig(img, format="png", dpi=300)
    img.seek(0)
    plt.close()
    return send_file(img, mimetype="image/png")

@app.route("/api/total_shots_per_player")
def total_shots_per_player():
    plt.figure(figsize=(8, 5))
    total_shots = [player_stats_df["player_1_number_of_shots"].max(), player_stats_df["player_2_number_of_shots"].max()]
    players = ["Player 1", "Player 2"]
    sns.barplot(x=players, y=total_shots, palette="viridis")
    plt.xlabel("Player")
    plt.ylabel("Total Shots")
    plt.title("Total Number of Shots Per Player")
    img = io.BytesIO()
    plt.savefig(img, format="png", dpi=300)
    img.seek(0)
    plt.close()
    return send_file(img, mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True)
