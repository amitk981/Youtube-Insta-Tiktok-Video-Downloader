#!/usr/bin/env python3
"""
YouTube Cookie Extractor
This script extracts YouTube cookies from your browser and formats them for Render
"""

import browser_cookie3
import json

def extract_youtube_cookies():
    """Extract YouTube cookies from Chrome browser"""
    print("🔍 Extracting YouTube cookies from Chrome...")
    
    try:
        # Try Chrome first
        cookies = browser_cookie3.chrome(domain_name='youtube.com')
        cookie_dict = {}
        
        for cookie in cookies:
            cookie_dict[cookie.name] = cookie.value
        
        if cookie_dict:
            print(f"✅ Found {len(cookie_dict)} YouTube cookies!")
            
            # Convert to Netscape format (what yt-dlp expects)
            netscape_cookies = "# Netscape HTTP Cookie File\n"
            for cookie in cookies:
                netscape_cookies += f".youtube.com\tTRUE\t/\t{'TRUE' if cookie.secure else 'FALSE'}\t{int(cookie.expires) if cookie.expires else 0}\t{cookie.name}\t{cookie.value}\n"
            
            # Save to file
            with open('youtube_cookies.txt', 'w') as f:
                f.write(netscape_cookies)
            
            print("✅ Cookies saved to youtube_cookies.txt")
            print("\n📋 Next steps:")
            print("1. The file 'youtube_cookies.txt' has been created")
            print("2. Copy its contents")
            print("3. Add it as YOUTUBE_COOKIES environment variable in Render")
            
            return netscape_cookies
        else:
            print("❌ No YouTube cookies found. Make sure you're logged into YouTube in Chrome.")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Make sure:")
        print("  - You're logged into YouTube in Chrome")
        print("  - Chrome is closed")
        print("  - You have browser_cookie3 installed: pip install browser-cookie3")
        return None

if __name__ == "__main__":
    extract_youtube_cookies()
