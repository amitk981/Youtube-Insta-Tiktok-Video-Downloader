#!/usr/bin/env python3
"""
Instagram Cookie Extractor
This script extracts Instagram cookies from your browser and formats them for Render
"""

import browser_cookie3

def extract_instagram_cookies():
    """Extract Instagram cookies from Chrome browser"""
    print("🔍 Extracting Instagram cookies from Chrome...")
    
    try:
        # Try Chrome first
        cookies = browser_cookie3.chrome(domain_name='instagram.com')
        cookie_dict = {}
        
        for cookie in cookies:
            cookie_dict[cookie.name] = cookie.value
        
        if cookie_dict:
            print(f"✅ Found {len(cookie_dict)} Instagram cookies!")
            
            # Convert to Netscape format (what yt-dlp expects)
            netscape_cookies = "# Netscape HTTP Cookie File\n"
            for cookie in cookies:
                netscape_cookies += f".instagram.com\tTRUE\t/\t{'TRUE' if cookie.secure else 'FALSE'}\t{int(cookie.expires) if cookie.expires else 0}\t{cookie.name}\t{cookie.value}\n"
            
            # Save to file
            with open('instagram_cookies.txt', 'w') as f:
                f.write(netscape_cookies)
            
            print("✅ Cookies saved to instagram_cookies.txt")
            print("\n📋 Next steps:")
            print("1. The file 'instagram_cookies.txt' has been created")
            print("2. Copy its contents")
            print("3. Add it as INSTAGRAM_COOKIES environment variable in Render")
            
            return netscape_cookies
        else:
            print("❌ No Instagram cookies found. Make sure you're logged into Instagram in Chrome.")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Make sure:")
        print("  - You're logged into Instagram in Chrome")
        print("  - Chrome is closed")
        return None

if __name__ == "__main__":
    extract_instagram_cookies()
