#!/usr/bin/env python3
"""
Digital Clock Application with Multiple Timezone Support
Displays current time in various time zones with real-time updates
"""

import tkinter as tk
from tkinter import font
from datetime import datetime
import pytz
from typing import List, Dict


class DigitalClock:
    """A digital clock that displays time in multiple timezones"""
    
    def __init__(self, root: tk.Tk, timezones: List[str] = None):
        """
        Initialize the digital clock
        
        Args:
            root: The Tkinter root window
            timezones: List of timezone strings (e.g., ['UTC', 'US/Eastern', 'Asia/Tokyo'])
        """
        self.root = root
        self.root.title("Digital Clock - Multiple Timezones")
        self.root.geometry("600x400")
        self.root.configure(bg="#1a1a1a")
        
        # Default timezones if none provided
        if timezones is None:
            timezones = [
                'UTC',
                'US/Eastern',
                'US/Central',
                'US/Mountain',
                'US/Pacific',
                'Europe/London',
                'Europe/Paris',
                'Asia/Tokyo',
                'Asia/Shanghai',
                'Australia/Sydney'
            ]
        
        self.timezones = timezones
        self.clock_labels: Dict[str, tk.Label] = {}
        self.setup_ui()
        self.update_time()
    
    def setup_ui(self) -> None:
        """Setup the user interface with timezone labels and time displays"""
        # Title
        title_font = font.Font(family="Helvetica", size=20, weight="bold")
        title_label = tk.Label(
            self.root,
            text="World Clock",
            font=title_font,
            fg="#00ff00",
            bg="#1a1a1a"
        )
        title_label.pack(pady=10)
        
        # Create a frame for the clocks
        clocks_frame = tk.Frame(self.root, bg="#1a1a1a")
        clocks_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create clock entries for each timezone
        time_font = font.Font(family="Courier New", size=14, weight="bold")
        tz_font = font.Font(family="Helvetica", size=10)
        
        for tz in self.timezones:
            # Timezone label
            tz_label = tk.Label(
                clocks_frame,
                text=f"{tz}:",
                font=tz_font,
                fg="#888888",
                bg="#1a1a1a",
                width=20,
                anchor="w"
            )
            tz_label.pack(anchor="w", pady=5)
            
            # Time display
            time_label = tk.Label(
                clocks_frame,
                text="00:00:00",
                font=time_font,
                fg="#00ff00",
                bg="#0a0a0a",
                anchor="w",
                padx=10,
                pady=5
            )
            time_label.pack(anchor="w", fill=tk.X, padx=20, pady=(0, 10))
            
            self.clock_labels[tz] = time_label
    
    def update_time(self) -> None:
        """Update the time display for all timezones"""
        for tz_str, label in self.clock_labels.items():
            try:
                tz = pytz.timezone(tz_str)
                current_time = datetime.now(tz)
                time_str = current_time.strftime("%H:%M:%S")
                date_str = current_time.strftime("%Y-%m-%d")
                label.config(text=f"{time_str}  ({date_str})")
            except pytz.exceptions.UnknownTimeZoneError:
                label.config(text="Invalid timezone")
        
        # Schedule the next update (every 1000ms = 1 second)
        self.root.after(1000, self.update_time)
    
    def run(self) -> None:
        """Start the clock application"""
        self.root.mainloop()


class DigitalClockCLI:
    """Command-line version of the digital clock"""
    
    def __init__(self, timezones: List[str] = None):
        """
        Initialize the CLI clock
        
        Args:
            timezones: List of timezone strings
        """
        if timezones is None:
            timezones = [
                'UTC',
                'US/Eastern',
                'US/Pacific',
                'Europe/London',
                'Asia/Tokyo'
            ]
        self.timezones = timezones
    
    def display(self) -> None:
        """Display current time in all timezones"""
        print("\n" + "=" * 60)
        print(" " * 15 + "WORLD CLOCK")
        print("=" * 60)
        
        for tz_str in self.timezones:
            try:
                tz = pytz.timezone(tz_str)
                current_time = datetime.now(tz)
                time_str = current_time.strftime("%H:%M:%S")
                date_str = current_time.strftime("%Y-%m-%d %A")
                offset = current_time.strftime("%z")
                print(f"{tz_str:<20} | {time_str} | {date_str} | UTC{offset}")
            except pytz.exceptions.UnknownTimeZoneError:
                print(f"{tz_str:<20} | Invalid timezone")
        
        print("=" * 60 + "\n")
    
    def run_continuous(self, interval: int = 1) -> None:
        """
        Run the clock continuously with updates
        
        Args:
            interval: Update interval in seconds
        """
        import time
        try:
            while True:
                self.display()
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\nClock stopped.")


if __name__ == "__main__":
    import sys
    
    # Check command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        # Run CLI version
        clock = DigitalClockCLI()
        clock.run_continuous(interval=1)
    else:
        # Run GUI version
        root = tk.Tk()
        clock = DigitalClock(root)
        clock.run()
