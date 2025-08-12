#!/usr/bin/env python3
"""
DataDash Lowerthird Generation Service
Core video processing logic adapted from our eyebrow work
"""

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import math
import os

class DataDashRenderer:
    def __init__(self, style="default"):
        self.width = 1920
        self.height = 1080
        self.fps = 30  # Optimized for smooth rendering
        self.style = style
        
        # Professional brand color schemes
        self.colors = {
            "default": {
                "primary": (45, 151, 255),      # Vibrant blue
                "secondary": (30, 100, 200),    # Deeper blue
                "accent": (200, 220, 255),      # Light blue
                "white": (255, 255, 255),
                "dark": (25, 35, 45),           # Dark blue-gray
                "background": (0, 0, 0)
            },
            "minimal": {
                "primary": (60, 70, 80),        # Sophisticated gray
                "secondary": (40, 50, 60),      # Darker gray
                "accent": (180, 190, 200),      # Light gray
                "white": (255, 255, 255),
                "dark": (30, 35, 40),           # Charcoal
                "background": (0, 0, 0)
            },
            "corporate": {
                "primary": (0, 84, 166),        # Professional blue
                "secondary": (0, 56, 110),      # Navy blue
                "accent": (120, 170, 220),      # Light corporate
                "white": (255, 255, 255),
                "dark": (20, 30, 50),           # Dark navy
                "background": (0, 0, 0)
            },
            "tech": {
                "primary": (0, 230, 118),       # Bright tech green
                "secondary": (0, 180, 90),      # Forest green
                "accent": (150, 255, 200),      # Light mint
                "white": (255, 255, 255),
                "dark": (15, 40, 25),           # Dark green
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
    
    def create_gradient(self, width, height, color1, color2, direction='horizontal'):
        """Create a gradient background"""
        gradient = Image.new('RGB', (width, height), color1)
        draw = ImageDraw.Draw(gradient)
        
        if direction == 'horizontal':
            for x in range(width):
                r = int(color1[0] + (color2[0] - color1[0]) * x / width)
                g = int(color1[1] + (color2[1] - color1[1]) * x / width)
                b = int(color1[2] + (color2[2] - color1[2]) * x / width)
                draw.line([(x, 0), (x, height)], fill=(r, g, b))
        else:  # vertical
            for y in range(height):
                r = int(color1[0] + (color2[0] - color1[0]) * y / height)
                g = int(color1[1] + (color2[1] - color1[1]) * y / height)
                b = int(color1[2] + (color2[2] - color1[2]) * y / height)
                draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        return gradient
    
    def create_professional_logo(self, size, colors, alpha, text="LT"):
        """Create a professional logo with gradient background"""
        logo_img = Image.new('RGBA', (size * 2, size), (0, 0, 0, 0))
        
        # Create gradient background
        gradient = self.create_gradient(size * 2, size, colors["primary"], colors["secondary"])
        gradient_alpha = Image.new('L', (size * 2, size), int(200 * alpha))
        
        # Convert to RGBA and apply alpha
        gradient_rgba = gradient.convert('RGBA')
        gradient_rgba.putalpha(gradient_alpha)
        
        # Create rounded rectangle mask
        mask = Image.new('L', (size * 2, size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([0, 0, size * 2 - 1, size - 1], radius=12, fill=255)
        
        # Apply mask to gradient
        gradient_rgba.putalpha(ImageEnhance.Brightness(mask).enhance(alpha))
        logo_img = Image.alpha_composite(logo_img, gradient_rgba)
        
        # Add text
        draw = ImageDraw.Draw(logo_img)
        try:
            font_size = int(size * 0.5)
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Text with shadow effect
        text_color = (*colors["white"], int(255 * alpha))
        shadow_color = (*colors["dark"], int(100 * alpha))
        
        # Get text dimensions for centering
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (size * 2 - text_width) // 2
        y = (size - text_height) // 2
        
        # Draw shadow
        draw.text((x + 2, y + 2), text, font=font, fill=shadow_color)
        # Draw main text
        draw.text((x, y), text, font=font, fill=text_color)
        
        return logo_img
    
    def create_frame(self, frame_num, duration, main_title, subtitle):
        """Create a professional lowerthird frame with gradients and shadows"""
        total_frames = int(duration * self.fps)
        
        # Base frame
        base = Image.new('RGB', (self.width, self.height), self.current_colors["background"])
        overlay = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Animation progress
        t = frame_num / total_frames
        
        # Main bar animation (first 60% of duration)
        bar_duration = 0.6
        if t <= bar_duration:
            bar_t = t / bar_duration
            bar_progress = self.ease_in_out_sine(bar_t)
            
            # Animated gradient bar
            bar_width = int(600 * bar_progress)
            bar_x, bar_y, bar_height = 40, 830, 180
            
            if bar_width > 0:
                # Create gradient bar
                gradient_bar = self.create_gradient(bar_width, bar_height, 
                                                  self.current_colors["primary"], 
                                                  self.current_colors["secondary"])
                
                # Add rounded corners and shadow
                bar_img = Image.new('RGBA', (bar_width, bar_height), (0, 0, 0, 0))
                
                # Shadow layer
                shadow_img = Image.new('RGBA', (bar_width + 8, bar_height + 8), (0, 0, 0, 0))
                shadow_draw = ImageDraw.Draw(shadow_img)
                shadow_draw.rounded_rectangle([4, 4, bar_width + 4, bar_height + 4], 
                                            radius=15, fill=(*self.current_colors["dark"], 100))
                
                # Main bar with gradient
                bar_rgba = gradient_bar.convert('RGBA')
                mask = Image.new('L', (bar_width, bar_height), 0)
                mask_draw = ImageDraw.Draw(mask)
                mask_draw.rounded_rectangle([0, 0, bar_width - 1, bar_height - 1], radius=12, fill=255)
                bar_rgba.putalpha(mask)
                
                # Composite shadow and bar
                shadow_img.paste(bar_rgba, (0, 0), bar_rgba)
                overlay.paste(shadow_img, (bar_x - 4, bar_y - 4), shadow_img)
                
                # Add accent line on top
                accent_img = Image.new('RGBA', (bar_width, 4), (*self.current_colors["accent"], 200))
                overlay.paste(accent_img, (bar_x, bar_y), accent_img)
        
        # Load fonts with better sizing
        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 52)
            subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
        except:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
        
        # Logo animation (starts at 15% duration)
        logo_start = 0.15
        if t > logo_start:
            logo_t = min((t - logo_start) / 0.4, 1.0)
            logo_alpha = self.ease_out_quart(logo_t)
            
            professional_logo = self.create_professional_logo(70, self.current_colors, logo_alpha)
            overlay.paste(professional_logo, (60, 845), professional_logo)
        
        # Title animation with shadow (starts at 25% duration)
        title_start = 0.25
        if t > title_start:
            title_t = min((t - title_start) / 0.35, 1.0)
            title_alpha = self.ease_out_quart(title_t)
            
            # Text positioning
            title_x, title_y = 220, 845
            
            # Shadow effect
            shadow_color = (*self.current_colors["dark"], int(150 * title_alpha))
            draw.text((title_x + 3, title_y + 3), main_title, font=title_font, fill=shadow_color)
            
            # Main title with gradient effect simulation
            title_color = (*self.current_colors["white"], int(255 * title_alpha))
            draw.text((title_x, title_y), main_title, font=title_font, fill=title_color)
        
        # Subtitle animation with shadow (starts at 40% duration)
        subtitle_start = 0.4
        if t > subtitle_start:
            subtitle_t = min((t - subtitle_start) / 0.35, 1.0)
            subtitle_alpha = self.ease_out_quart(subtitle_t)
            
            # Text positioning
            subtitle_x, subtitle_y = 220, 900
            
            # Shadow effect
            shadow_color = (*self.current_colors["dark"], int(120 * subtitle_alpha))
            draw.text((subtitle_x + 2, subtitle_y + 2), subtitle, font=subtitle_font, fill=shadow_color)
            
            # Main subtitle
            subtitle_color = (*self.current_colors["accent"], int(255 * subtitle_alpha))
            draw.text((subtitle_x, subtitle_y), subtitle, font=subtitle_font, fill=subtitle_color)
        
        # Add subtle glow effect around text area
        if t > 0.3:
            glow_alpha = min((t - 0.3) / 0.3, 0.3)
            glow_img = Image.new('RGBA', (580, 120), (*self.current_colors["primary"], int(30 * glow_alpha)))
            blur_glow = glow_img.filter(ImageFilter.GaussianBlur(radius=15))
            overlay.paste(blur_glow, (200, 835), blur_glow)
        
        # Composite and return
        final_img = Image.alpha_composite(base.convert('RGBA'), overlay).convert('RGB')
        return cv2.cvtColor(np.array(final_img), cv2.COLOR_RGB2BGR)

def generate_lowerthird(main_title, subtitle, output_name, duration=4.0, style="default"):
    """
    Generate a DataDash lowerthird video
    Returns the path to the generated video file
    """
    # Setup paths - prioritize container path
    output_dir = os.getenv("OUTPUT_DIR", "/app/outputs")
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