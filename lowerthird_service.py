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
    
    def create_premium_background(self, width, height, t, colors):
        """Create animated premium tech background with subtle movement"""
        bg = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(bg)
        
        # Animated gradient waves - very subtle for Apple cleanliness
        if t > 0.1:  # Start subtle background animation
            bg_alpha = min((t - 0.1) / 0.3, 0.05)  # Very subtle, max 5% opacity
            
            # Create flowing gradient lines
            for i in range(3):
                y_offset = int(100 * math.sin((t * 2 + i) * math.pi)) 
                y_pos = self.height - 200 + y_offset + (i * 40)
                
                if 0 <= y_pos <= self.height:
                    # Ultra-subtle gradient line
                    line_color = (*colors["primary"], int(30 * bg_alpha))
                    draw.ellipse([0, y_pos-20, width, y_pos+20], fill=line_color)
        
        # Premium edge glow that builds anticipation
        if t < 0.8:
            glow_progress = t / 0.8
            glow_alpha = int(20 * glow_progress)
            
            # Left edge premium glow
            for x in range(100):
                alpha = int(glow_alpha * (100-x) / 100)
                draw.rectangle([x, 0, x+1, height], fill=(*colors["primary"], alpha))
        
        return bg
    
    def create_frame(self, frame_num, duration, main_title, subtitle):
        """Create a premium tech reveal lowerthird with Apple-like smoothness"""
        total_frames = int(duration * self.fps)
        
        # Base frame with premium background
        base = Image.new('RGB', (self.width, self.height), self.current_colors["background"])
        
        # Animation progress with premium timing
        t = frame_num / total_frames
        
        # Add premium animated background
        premium_bg = self.create_premium_background(self.width, self.height, t, self.current_colors)
        base_rgba = base.convert('RGBA')
        base_with_bg = Image.alpha_composite(base_rgba, premium_bg)
        
        overlay = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Premium bar animation with Apple-like smoothness (delayed elegant reveal)
        bar_start = 0.2  # Delayed start for premium feel
        bar_duration = 0.5
        if t > bar_start and t <= (bar_start + bar_duration):
            bar_t = (t - bar_start) / bar_duration
            # Custom premium easing - starts slow, elegant acceleration, smooth settle
            bar_progress = self.ease_out_quart(bar_t)
            
            # Premium bar dimensions - more elegant proportions
            bar_width = int(650 * bar_progress)
            bar_x, bar_y, bar_height = 40, 820, 200
            
            if bar_width > 0:
                # Multi-layered premium bar construction
                
                # Deep shadow layer for premium depth
                deep_shadow = Image.new('RGBA', (bar_width + 16, bar_height + 16), (0, 0, 0, 0))
                deep_shadow_draw = ImageDraw.Draw(deep_shadow)
                deep_shadow_draw.rounded_rectangle([8, 8, bar_width + 8, bar_height + 8], 
                                                 radius=20, fill=(0, 0, 0, 40))
                
                # Medium shadow for layered depth
                med_shadow = Image.new('RGBA', (bar_width + 8, bar_height + 8), (0, 0, 0, 0))
                med_shadow_draw = ImageDraw.Draw(med_shadow)
                med_shadow_draw.rounded_rectangle([4, 4, bar_width + 4, bar_height + 4], 
                                                radius=18, fill=(0, 0, 0, 80))
                
                # Premium gradient with more sophistication
                premium_gradient = self.create_gradient(bar_width, bar_height,
                                                      self.current_colors["primary"],
                                                      self.current_colors["secondary"])
                
                # Glass overlay layer for premium Apple-like material
                glass_overlay = Image.new('RGBA', (bar_width, bar_height), (255, 255, 255, 25))
                
                # Main bar with perfect rounded corners
                bar_rgba = premium_gradient.convert('RGBA')
                mask = Image.new('L', (bar_width, bar_height), 0)
                mask_draw = ImageDraw.Draw(mask)
                mask_draw.rounded_rectangle([0, 0, bar_width - 1, bar_height - 1], radius=16, fill=255)
                bar_rgba.putalpha(mask)
                glass_overlay.putalpha(mask)
                
                # Composite all layers for premium depth
                overlay.paste(deep_shadow, (bar_x - 8, bar_y - 8), deep_shadow)
                overlay.paste(med_shadow, (bar_x - 4, bar_y - 4), med_shadow)
                overlay.paste(bar_rgba, (bar_x, bar_y), bar_rgba)
                overlay.paste(glass_overlay, (bar_x, bar_y), glass_overlay)
                
                # Premium accent highlight - thinner and more sophisticated
                highlight_height = 3
                accent_img = Image.new('RGBA', (bar_width, highlight_height), 
                                     (*self.current_colors["accent"], int(180 * bar_progress)))
                overlay.paste(accent_img, (bar_x, bar_y), accent_img)
        
        # Load fonts with better sizing
        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 52)
            subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
        except:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
        
        # Premium logo animation with elegant materialization
        logo_start = 0.4  # Starts after bar is mostly revealed
        logo_duration = 0.4
        if t > logo_start:
            logo_t = min((t - logo_start) / logo_duration, 1.0)
            
            # Elegant emergence with multiple phases
            if logo_t < 0.3:
                # Phase 1: Subtle glow appears first
                glow_alpha = self.ease_in_out_sine(logo_t / 0.3) * 0.3
                logo_size = 75
                glow_size = int(logo_size * 1.2)
                
                # Create glow halo
                glow_img = Image.new('RGBA', (glow_size * 2, glow_size), (0, 0, 0, 0))
                glow_draw = ImageDraw.Draw(glow_img)
                glow_draw.ellipse([glow_size//4, glow_size//4, glow_size*1.75, glow_size*0.75], 
                                fill=(*self.current_colors["primary"], int(60 * glow_alpha)))
                glow_blurred = glow_img.filter(ImageFilter.GaussianBlur(radius=15))
                overlay.paste(glow_blurred, (50, 835), glow_blurred)
                
            elif logo_t < 0.7:
                # Phase 2: Logo materializes with scale
                material_t = (logo_t - 0.3) / 0.4
                scale_progress = self.ease_out_quart(material_t)
                logo_alpha = scale_progress
                
                # Slight scale animation for premium feel
                base_size = 75
                current_size = int(base_size * (0.8 + 0.2 * scale_progress))
                
                professional_logo = self.create_professional_logo(current_size, self.current_colors, logo_alpha)
                logo_x = 60 - int((current_size - base_size) * 0.5)
                logo_y = 845 - int((current_size - base_size) * 0.3)
                overlay.paste(professional_logo, (logo_x, logo_y), professional_logo)
                
            else:
                # Phase 3: Final settle with full opacity
                settle_t = (logo_t - 0.7) / 0.3
                final_alpha = 0.8 + 0.2 * self.ease_out_quart(settle_t)
                
                professional_logo = self.create_professional_logo(75, self.current_colors, final_alpha)
                overlay.paste(professional_logo, (60, 845), professional_logo)
        
        # Premium title animation with elegant character-by-character reveal
        title_start = 0.6  # Starts after logo materialization
        title_duration = 0.5
        if t > title_start:
            title_t = min((t - title_start) / title_duration, 1.0)
            
            # Calculate how many characters to reveal
            title_length = len(main_title)
            chars_to_show = int(title_length * self.ease_out_quart(title_t))
            visible_title = main_title[:chars_to_show]
            
            # Position with better spacing for premium look
            title_x, title_y = 230, 835
            
            if visible_title:
                # Premium shadow with multiple layers for depth
                for i, offset in enumerate([(4, 4), (2, 2)]):
                    shadow_alpha = int((80 - i*20) * title_t)
                    shadow_color = (*self.current_colors["dark"], shadow_alpha)
                    draw.text((title_x + offset[0], title_y + offset[1]), visible_title, 
                             font=title_font, fill=shadow_color)
                
                # Main title with premium white
                title_alpha = min(title_t * 1.2, 1.0)  # Slightly faster alpha ramp
                title_color = (*self.current_colors["white"], int(255 * title_alpha))
                draw.text((title_x, title_y), visible_title, font=title_font, fill=title_color)
                
                # Add subtle glow to current character being revealed
                if chars_to_show < title_length and chars_to_show > 0:
                    current_char = main_title[chars_to_show-1:chars_to_show]
                    try:
                        # Get position of current character
                        prev_text = main_title[:chars_to_show-1]
                        prev_bbox = draw.textbbox((0, 0), prev_text, font=title_font)
                        char_x = title_x + (prev_bbox[2] - prev_bbox[0])
                        
                        # Subtle glow on revealing character
                        glow_color = (*self.current_colors["primary"], int(60 * title_t))
                        for glow_offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                            draw.text((char_x + glow_offset[0], title_y + glow_offset[1]), 
                                     current_char, font=title_font, fill=glow_color)
                    except:
                        pass
        
        # Premium subtitle with word-by-word reveal
        subtitle_start = 0.8  # Starts near end of title reveal
        subtitle_duration = 0.4
        if t > subtitle_start:
            subtitle_t = min((t - subtitle_start) / subtitle_duration, 1.0)
            
            # Word-by-word reveal for sophistication
            words = subtitle.split()
            words_to_show = int(len(words) * self.ease_out_quart(subtitle_t))
            visible_subtitle = " ".join(words[:words_to_show])
            
            # Position with elegant spacing
            subtitle_x, subtitle_y = 230, 890
            
            if visible_subtitle:
                # Elegant shadow
                shadow_alpha = int(100 * subtitle_t)
                shadow_color = (*self.current_colors["dark"], shadow_alpha)
                draw.text((subtitle_x + 2, subtitle_y + 2), visible_subtitle, 
                         font=subtitle_font, fill=shadow_color)
                
                # Main subtitle with accent color
                subtitle_alpha = min(subtitle_t * 1.3, 1.0)
                subtitle_color = (*self.current_colors["accent"], int(240 * subtitle_alpha))
                draw.text((subtitle_x, subtitle_y), visible_subtitle, 
                         font=subtitle_font, fill=subtitle_color)
        
        # Premium ambient glow that builds throughout animation
        if t > 0.5:
            glow_alpha = min((t - 0.5) / 0.4, 0.2)  # More subtle for Apple cleanliness
            
            # Create sophisticated glow area
            glow_width, glow_height = 700, 140
            glow_img = Image.new('RGBA', (glow_width, glow_height), (0, 0, 0, 0))
            glow_draw = ImageDraw.Draw(glow_img)
            
            # Multi-layer glow for premium depth
            center_x, center_y = glow_width // 2, glow_height // 2
            for radius in [60, 40, 20]:
                alpha = int(20 * glow_alpha * (60 - radius) / 40)
                glow_draw.ellipse([center_x - radius, center_y - radius, 
                                 center_x + radius, center_y + radius],
                                fill=(*self.current_colors["primary"], alpha))
            
            # Apply sophisticated blur
            premium_glow = glow_img.filter(ImageFilter.GaussianBlur(radius=25))
            overlay.paste(premium_glow, (190, 815), premium_glow)
        
        # Final composition with premium background
        final_img = Image.alpha_composite(base_with_bg, overlay).convert('RGB')
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