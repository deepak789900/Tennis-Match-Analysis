import numpy as np
import cv2

def show_committee_paneles(output_video_frames, player_stats):
    """
    Displays player statistics on a "Player Selection Committee Panel" for all frames in the video.

    Parameters:
        output_video_frames (list of np.array): List of video frames.
        player_stats (pd.DataFrame): DataFrame containing player statistics for each frame.

    Returns:
        list of np.array: Video frames with the committee panel added.
    """
    # Panel dimensions
    panel_width = 600
    panel_color = (50, 50, 50)  # Dark gray background
    text_color = (255, 255, 255)  # White text
    header_color = (200, 200, 200)  # Light gray header text
    font = cv2.FONT_HERSHEY_SIMPLEX

    for i, frame in enumerate(output_video_frames):
        # Extract the corresponding player statistics for the current frame
        frame_stats = player_stats.iloc[i]

        # Create a blank panel
        panel_height = frame.shape[0]
        panel = np.zeros((panel_height, panel_width, 3), dtype=np.uint8)
        panel[:, :] = panel_color

        # Add title
        cv2.putText(panel, "Player Selection Committee Panel", (40, 40), font, 0.7, text_color, 2)

        # Add column headers
        cv2.putText(panel, "Stats", (20, 80), font, 0.6, header_color, 1)
        cv2.putText(panel, "Player 1", (140, 80), font, 0.6, header_color, 1)
        cv2.putText(panel, "Player 2", (260, 80), font, 0.6, header_color, 1)

        # Define the statistics to display
        stats = [
            ("Shot Speed", frame_stats['player_1_last_shot_speed'], frame_stats['player_2_last_shot_speed']),
            ("Avg. S Speed", frame_stats['player_1_average_shot_speed'], frame_stats['player_2_average_shot_speed']),
            ("Player Speed ", frame_stats['player_1_last_player_speed'], frame_stats['player_2_last_player_speed']),
            ("Avg. P Speed", frame_stats['player_1_average_player_speed'],frame_stats['player_2_average_player_speed']),
        ]

        # Display each statistic on the panel
        y_offset = 120
        for stat_name, p1_stat, p2_stat in stats:
            cv2.putText(panel, stat_name, (20, y_offset), font, 0.5, text_color, 1)
            cv2.putText(panel, f"{p1_stat:.1f}", (160, y_offset), font, 0.5, text_color, 1)
            cv2.putText(panel, f"{p2_stat:.1f}", (280, y_offset), font, 0.5, text_color, 1)
            y_offset += 50

        # Combine the panel with the current frame
        combined_frame = np.hstack((frame, panel))

        # Replace the current frame with the combined frame
        output_video_frames[i] = combined_frame

    return output_video_frames

# Example Usage:
# output_video_frames = show_committee_paneles(output_video_frames, player_stats_data_df)
