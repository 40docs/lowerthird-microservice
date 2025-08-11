#!/usr/bin/env python3
"""
DataDash Lowerthird Generation Service
Core video processing logic adapted from our eyebrow work
"""

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import math
import os

class DataDashRenderer:
    def __init__(self, style="default"):
        self.width = 1920
        self.height = 1080
        self.fps = 30  # Optimized for smooth rendering
        self.style = style
        
        # DataDash brand colors
        self.colors = {
            "default": {
                "primary": (45, 151, 255),      # DataDash blue
                "accent": (200, 220, 255),      # Light blue
                "white": (255, 255, 255),
                "background": (0, 0, 0)
            },
            "minimal": {
                "primary": (80, 80, 80),        # Gray
                "accent": (150, 150, 150),      # Light gray
                "white": (255, 255, 255),
                "background": (0, 0, 0)
            },
            "corporate": {
                "primary": (0, 64, 128),        # Corporate blue
                "accent": (100, 150, 200),      # Light corporate
                "white": (255, 255, 255),
                "background": (0, 0, 0)
            },
            "tech": {
                "primary": (0, 255, 127),       # Tech green
                "accent": (127, 255, 191),      # Light green
                "white": (255, 255, 255),
                "background": (0, 0, 0)
            }
        }
        
        self.current_colors = self.colors.get(style, self.colors["default"])
        
    def ease_out_quart(self, t):
        """Smooth quartic ease-out for natural animation"""
        return 1 - (1 - t) ** 4
    
    def ease_in_out_sine(self, t):
        """Sine wave easing for most natural motion"""
        return -(math.cos(math.pi * t) - 1) / 2
    
    def create_dd_logo(self, size, color, alpha):
        """Create DataDash DD logo"""
        logo_img = Image.new('RGBA', (size * 2, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(logo_img)
        
        logo_color = (*color, int(255 * alpha))
        
        try:
            font_size = int(size * 0.6)
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Draw DD letters
        draw.text((2, size // 4), "D", font=font, fill=logo_color)
        draw.text((size // 2 + 2, size // 4), "D", font=font, fill=logo_color)
        
        # Background shape
        bg_color = (*color, int(80 * alpha))
        padding = 8
        draw.rounded_rectangle([0, 0, size * 2 - 1, size - 1], 
                              radius=8, fill=bg_color, outline=logo_color, width=2)
        
        return logo_img
    
    def create_frame(self, frame_num, duration, main_title, subtitle):
        """Create a single frame of the lowerthird"""
        total_frames = int(duration * self.fps)
        
        # Base frame
        base = Image.new('RGB', (self.width, self.height), self.current_colors["background"])
        overlay = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Animation progress
        t = frame_num / total_frames
        
        # Bar animation (first 60% of duration)
        bar_duration = 0.6
        if t <= bar_duration:
            bar_t = t / bar_duration
            bar_progress = self.ease_in_out_sine(bar_t)
            
            bar_width = int(500 * bar_progress)
            bar_x, bar_y, bar_height = 50, 850, 150
            
            if bar_width > 0:
                draw.rectangle([bar_x, bar_y, bar_x + bar_width, bar_y + bar_height],
                             fill=(*self.current_colors["primary"], 255))
        
        # Load fonts
        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
            subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
        except:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
        
        # Logo animation (starts at 20% duration)
        logo_start = 0.2
        if t > logo_start:
            logo_t = min((t - logo_start) / 0.3, 1.0)
            logo_alpha = self.ease_out_quart(logo_t)
            
            dd_logo = self.create_dd_logo(60, self.current_colors["primary"], logo_alpha)
            overlay.paste(dd_logo, (70, 860), dd_logo)
        
        # Title animation (starts at 25% duration)
        title_start = 0.25
        if t > title_start:
            title_t = min((t - title_start) / 0.3, 1.0)
            title_alpha = self.ease_out_quart(title_t)
            
            title_color = (*self.current_colors["white"], int(255 * title_alpha))
            draw.text((200, 860), main_title, font=title_font, fill=title_color)
        
        # Subtitle animation (starts at 40% duration)
        subtitle_start = 0.4
        if t > subtitle_start:
            subtitle_t = min((t - subtitle_start) / 0.3, 1.0)
            subtitle_alpha = self.ease_out_quart(subtitle_t)
            
            subtitle_color = (*self.current_colors["accent"], int(255 * subtitle_alpha))
            draw.text((200, 920), subtitle, font=subtitle_font, fill=subtitle_color)
        
        # Composite and return
        final_img = Image.alpha_composite(base.convert('RGBA'), overlay).convert('RGB')
        return cv2.cvtColor(np.array(final_img), cv2.COLOR_RGB2BGR)

def generate_lowerthird(main_title, subtitle, output_name, duration=4.0, style="default"):
    """
    Generate a DataDash lowerthird video
    Returns the path to the generated video file
    """
    # Setup paths
    output_dir = os.getenv("OUTPUT_DIR", "/app/outputs")
    if not os.path.exists(output_dir) and os.getcwd():
        # Fallback to local outputs for testing
        output_dir = os.path.join(os.getcwd(), "outputs")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{output_name}.mp4")
    
    # Initialize renderer
    renderer = DataDashRenderer(style=style)
    total_frames = int(duration * renderer.fps)
    
    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(output_path, fourcc, renderer.fps, 
                           (renderer.width, renderer.height))
    
    if not writer.isOpened():
        raise Exception(f"Failed to create video writer for {output_path}")
    
    try:
        # Render all frames
        for frame_num in range(total_frames):
            frame = renderer.create_frame(frame_num, duration, main_title, subtitle)
            writer.write(frame)
        
        return output_path
        
    except Exception as e:
        raise Exception(f"Video generation failed: {str(e)}")
    
    finally:
        writer.release()

# Test function for standalone execution
if __name__ == "__main__":
    # Create test output
    test_path = generate_lowerthird(
        main_title="Test Title",
        subtitle="Test Subtitle", 
        output_name="test_lowerthird",
        duration=3.0,
        style="default"
    )
    print(f"Test video generated: {test_path}")