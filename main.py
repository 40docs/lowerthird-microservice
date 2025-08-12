#!/usr/bin/env python3
"""
DataDash Lowerthird Microservice
A Flask-based microservice for generating DataDash-branded lowerthird graphics for Fortinet/Forticloud community content
Follows the 40docs microservice architecture pattern
"""

from flask import Flask, request, jsonify
import os
from lowerthird_service import generate_lowerthird

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint for container orchestration"""
    return jsonify({"status": "ok"})

@app.route('/create-lowerthird', methods=['POST'])
def create_lowerthird():
    """
    Generate a DataDash lowerthird video for Fortinet/Forticloud content
    
    Expected JSON payload:
    {
        "main_title": "DataDash",
        "subtitle": "Fortinet Security Insights", 
        "output_name": "my_lowerthird",
        "duration": 4.0,
        "style": "cloud_blue"
    }
    """
    try:
        # Parse request data
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON payload provided"}), 400
        
        # Extract parameters with defaults
        main_title = data.get('main_title', 'DataDash')
        subtitle = data.get('subtitle', 'Fortinet Community Insights')
        output_name = data.get('output_name', 'lowerthird')
        duration = data.get('duration', 4.0)
        style = data.get('style', 'cloud_blue')
        
        # Validate inputs
        if not isinstance(duration, (int, float)) or duration <= 0:
            return jsonify({"error": "Duration must be a positive number"}), 400
            
        if len(main_title) > 100 or len(subtitle) > 100:
            return jsonify({"error": "Title or subtitle too long (max 100 chars)"}), 400
        
        # Generate lowerthird video
        video_path = generate_lowerthird(
            main_title=main_title,
            subtitle=subtitle,
            output_name=output_name,
            duration=duration,
            style=style
        )
        
        return jsonify({
            "status": "ok",
            "video": video_path,
            "parameters": {
                "main_title": main_title,
                "subtitle": subtitle,
                "duration": duration,
                "style": style
            }
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/styles', methods=['GET'])
def list_styles():
    """List available DataDash lowerthird styles"""
    return jsonify({
        "styles": [
            "cloud_blue",
            "secure_red", 
            "sase_purple",
            "connectivity_yellow"
        ]
    })

if __name__ == '__main__':
    # Ensure output directory exists
    output_dir = os.getenv("OUTPUT_DIR", "/app/outputs")
    os.makedirs(output_dir, exist_ok=True)
    
    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=False)