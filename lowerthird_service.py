#!/usr/bin/env python3
"""
DataDash Lowerthird Generation Service
Professional lowerthird graphics for DataDash community content about Fortinet/Forticloud
Uses Fortinet-inspired colors: secure red, cloud blue, sase purple, connectivity yellow
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
        
        # DataDash color schemes using Fortinet-inspired palette
        self.colors = {
            "cloud_blue": {
                "primary": (48, 127, 226),      # Cloud Blue #307FE2
                "secondary": (30, 90, 180),     # Deeper cloud blue
                "accent": (200, 220, 255),      # Light blue accent
                "white": (255, 255, 255),
                "dark": (20, 40, 80),           # Dark blue for depth
                "background": (0, 0, 0)         # Black for solid background
            },
            "secure_red": {
                "primary": (218, 41, 28),       # Secure Red #DA291C
                "secondary": (160, 30, 20),     # Deeper secure red
                "accent": (255, 180, 170),      # Light red accent
                "white": (255, 255, 255),
                "dark": (80, 15, 10),           # Dark red
                "background": (0, 0, 0)         # Black background
            },
            "sase_purple": {
                "primary": (144, 99, 205),      # SASE Purple #9063CD
                "secondary": (100, 70, 150),    # Deeper purple
                "accent": (200, 180, 230),      # Light purple accent
                "white": (255, 255, 255),
                "dark": (40, 30, 80),           # Dark purple
                "background": (0, 0, 0)         # Black background
            },
            "connectivity_yellow": {
                "primary": (255, 185, 0),       # Connectivity Yellow #FFB900
                "secondary": (200, 145, 0),     # Deeper yellow
                "accent": (255, 230, 150),      # Light yellow accent
                "white": (255, 255, 255),
                "dark": (80, 60, 0),            # Dark yellow/brown
                "background": (0, 0, 0)         # Black background
            }
        }
        
        self.current_colors = self.colors.get(style, self.colors["cloud_blue"])
        
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
    
    def create_professional_logo(self, size, colors, alpha, text="DD"):
        """Create a professional DataDash logo with gradient background and prominent DD text"""
        logo_img = Image.new('RGBA', (size * 2, size), (0, 0, 0, 0))
        
        # Create gradient background
        gradient = self.create_gradient(size * 2, size, colors["primary"], colors["secondary"])
        gradient_alpha = Image.new('L', (size * 2, size), int(220 * alpha))
        
        # Convert to RGBA and apply alpha
        gradient_rgba = gradient.convert('RGBA')
        gradient_rgba.putalpha(gradient_alpha)
        
        # Create rounded rectangle mask
        mask = Image.new('L', (size * 2, size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([0, 0, size * 2 - 1, size - 1], radius=15, fill=255)
        
        # Apply mask to gradient
        gradient_rgba.putalpha(ImageEnhance.Brightness(mask).enhance(alpha))
        logo_img = Image.alpha_composite(logo_img, gradient_rgba)
        
        # Add DataDash DD text with multiple font fallbacks
        draw = ImageDraw.Draw(logo_img)
        font_size = int(size * 0.6)  # Larger font size for visibility
        font = None
        
        # Try multiple font paths for better compatibility
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
            "/System/Library/Fonts/Helvetica.ttc"
        ]
        
        for font_path in font_paths:
            try:
                font = ImageFont.truetype(font_path, font_size)
                break
            except:
                continue
        
        # Fallback to default font if no TrueType fonts found
        if font is None:
            try:
                font = ImageFont.load_default()
            except:
                # Ultimate fallback - create text manually
                return logo_img
        
        # Enhanced text colors for better visibility
        text_color = (*colors["white"], int(255 * alpha))
        shadow_color = (*colors["dark"], int(150 * alpha))
        
        # Create modern intersecting DD logo instead of side-by-side text
        # Get single D dimensions for positioning
        try:
            single_d_bbox = draw.textbbox((0, 0), "D", font=font)
            d_width = single_d_bbox[2] - single_d_bbox[0]
            d_height = single_d_bbox[3] - single_d_bbox[1]
        except:
            # Fallback sizing
            d_width = font_size // 2
            d_height = font_size
        
        # Calculate positions for intersecting D's
        center_x = size  # Center of the logo
        center_y = size // 2
        
        # Offset for intersection - first D slightly left and up, second D slightly right and down
        overlap_offset = int(d_width * 0.3)  # 30% overlap for modern look
        
        d1_x = center_x - d_width // 2 - overlap_offset // 2
        d1_y = center_y - d_height // 2 - 3
        
        d2_x = center_x - d_width // 2 + overlap_offset // 2  
        d2_y = center_y - d_height // 2 + 3
        
        # Draw shadows for both D's
        shadow_offsets = [(3, 3), (2, 2), (1, 1)]
        for offset in shadow_offsets:
            shadow_alpha = int(60 * alpha / len(shadow_offsets))
            shadow_col = (*colors["dark"], shadow_alpha)
            # First D shadow
            draw.text((d1_x + offset[0], d1_y + offset[1]), "D", font=font, fill=shadow_col)
            # Second D shadow
            draw.text((d2_x + offset[0], d2_y + offset[1]), "D", font=font, fill=shadow_col)
        
        # Draw glow effects for both D's
        glow_color = (*colors["primary"], int(80 * alpha))
        for glow_offset in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
            # First D glow
            draw.text((d1_x + glow_offset[0], d1_y + glow_offset[1]), "D", font=font, fill=glow_color)
            # Second D glow  
            draw.text((d2_x + glow_offset[0], d2_y + glow_offset[1]), "D", font=font, fill=glow_color)
        
        # Draw the first D with primary color
        first_d_color = (*colors["white"], int(255 * alpha))
        draw.text((d1_x, d1_y), "D", font=font, fill=first_d_color)
        
        # Draw the second D with accent color for contrast
        second_d_color = (*colors["accent"], int(240 * alpha))
        draw.text((d2_x, d2_y), "D", font=font, fill=second_d_color)
        
        # Add subtle outline to make intersection more visible
        outline_color = (*colors["primary"], int(150 * alpha))
        for outline_offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            # Outline for first D
            draw.text((d1_x + outline_offset[0], d1_y + outline_offset[1]), "D", font=font, fill=outline_color)
            # Outline for second D
            draw.text((d2_x + outline_offset[0], d2_y + outline_offset[1]), "D", font=font, fill=outline_color)
        
        # Redraw main D's on top for crisp appearance
        draw.text((d1_x, d1_y), "D", font=font, fill=first_d_color)
        draw.text((d2_x, d2_y), "D", font=font, fill=second_d_color)
        
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