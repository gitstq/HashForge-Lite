#!/usr/bin/env python3
"""
HashForge TUI Dashboard - Interactive Terminal User Interface
"""

import sys
import curses
from typing import Optional

# Add parent directory to path
sys.path.insert(0, str(__file__).parent.parent.parent)

from hashforge.core import HashCalculator, Encoder, CryptoEngine, PasswordGenerator


class HashForgeTUI:
    """Interactive TUI Dashboard for HashForge."""
    
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.hash_calc = HashCalculator()
        self.encoder = Encoder()
        self.crypto = CryptoEngine()
        self.pwd_gen = PasswordGenerator()
        
        # State
        self.current_tab = 0
        self.tabs = ['Hash', 'Encode', 'Encrypt', 'Password']
        self.input_text = ""
        self.output_text = ""
        self.key_text = ""
        self.selected_algo = 0
        self.message = ""
        
        # Colors
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)    # Title
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Success
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Warning
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLUE)    # Selected tab
        
        # Algorithms per tab
        self.algorithms = [
            HashCalculator.list_algorithms(),  # Hash
            ['base64', 'base32', 'hex', 'url', 'ascii', 'binary'],  # Encode
            ['xor', 'rot13', 'caesar', 'vigenere'],  # Encrypt
            ['generate', 'passphrase', 'pin', 'analyze']  # Password
        ]
    
    def draw_header(self):
        """Draw header with title."""
        self.stdscr.addstr(0, 2, "🔐 HashForge", curses.color_pair(1) | curses.A_BOLD)
        self.stdscr.addstr(0, 20, f"v1.0.0 - Lightweight Hash & Encoding Toolkit", curses.A_DIM)
        
        # Draw tabs
        tab_width = 15
        for i, tab in enumerate(self.tabs):
            x = 2 + i * (tab_width + 2)
            if i == self.current_tab:
                self.stdscr.addstr(2, x, f" [{tab}] ", curses.color_pair(4) | curses.A_BOLD)
            else:
                self.stdscr.addstr(2, x, f"  {tab}  ", curses.A_DIM)
        
        self.stdscr.addstr(3, 2, "─" * 70, curses.A_DIM)
    
    def draw_input_section(self):
        """Draw input section."""
        self.stdscr.addstr(5, 2, "Input:", curses.A_BOLD)
        
        # Input box
        self.stdscr.addstr(6, 2, "┌" + "─" * 66 + "┐", curses.A_DIM)
        
        # Display input text (wrap if needed)
        display_text = self.input_text[:64]
        self.stdscr.addstr(7, 2, f"│ {display_text:<64}│")
        
        self.stdscr.addstr(8, 2, "└" + "─" * 66 + "┘", curses.A_DIM)
    
    def draw_algorithm_selector(self):
        """Draw algorithm selector."""
        self.stdscr.addstr(10, 2, "Algorithm:", curses.A_BOLD)
        
        algos = self.algorithms[self.current_tab]
        for i, algo in enumerate(algos[:8]):  # Show max 8
            x = 14 + i * 10
            if i == self.selected_algo:
                self.stdscr.addstr(10, x, f"[{algo}]", curses.color_pair(2) | curses.A_BOLD)
            else:
                self.stdscr.addstr(10, x, f" {algo} ", curses.A_DIM)
    
    def draw_key_input(self):
        """Draw key input for encryption."""
        if self.current_tab == 2:  # Encrypt tab
            self.stdscr.addstr(12, 2, "Key:", curses.A_BOLD)
            key_display = self.key_text[:60] if self.key_text else "(enter key)"
            self.stdscr.addstr(12, 8, f"[ {key_display} ]", curses.color_pair(3))
    
    def draw_output_section(self):
        """Draw output section."""
        self.stdscr.addstr(14, 2, "Output:", curses.A_BOLD)
        
        # Output box
        self.stdscr.addstr(15, 2, "┌" + "─" * 66 + "┐", curses.A_DIM)
        
        # Display output (multi-line)
        lines = self.output_text.split('\n')[:5]  # Max 5 lines
        for i, line in enumerate(lines):
            display_line = line[:64]
            self.stdscr.addstr(16 + i, 2, f"│ {display_line:<64}│")
        
        # Fill remaining lines
        for i in range(len(lines), 5):
            self.stdscr.addstr(16 + i, 2, "│" + " " * 66 + "│")
        
        self.stdscr.addstr(21, 2, "└" + "─" * 66 + "┘", curses.A_DIM)
    
    def draw_help(self):
        """Draw help section."""
        self.stdscr.addstr(23, 2, "Keys:", curses.A_BOLD)
        self.stdscr.addstr(23, 8, "[Tab] Switch tab  [←→] Change algo  [Enter] Execute  [C] Clear  [Q] Quit", curses.A_DIM)
        
        if self.message:
            self.stdscr.addstr(24, 2, self.message, curses.color_pair(2))
    
    def process_input(self):
        """Process current input and generate output."""
        try:
            if self.current_tab == 0:  # Hash
                algo = self.algorithms[0][self.selected_algo]
                self.hash_calc = HashCalculator(algo)
                self.output_text = self.hash_calc.hash_string(self.input_text)
                self.message = f"✓ {algo.upper()} hash calculated"
            
            elif self.current_tab == 1:  # Encode
                enc_type = self.algorithms[1][self.selected_algo]
                self.output_text = self.encoder.encode(self.input_text, enc_type)
                self.message = f"✓ {enc_type.upper()} encoded"
            
            elif self.current_tab == 2:  # Encrypt
                algo = self.algorithms[2][self.selected_algo]
                if not self.key_text:
                    self.message = "⚠ Please enter a key"
                    return
                self.output_text = self.crypto.encrypt(self.input_text, algo, self.key_text)
                self.message = f"✓ {algo.upper()} encrypted"
            
            elif self.current_tab == 3:  # Password
                action = self.algorithms[3][self.selected_algo]
                if action == 'generate':
                    self.output_text = self.pwd_gen.generate(length=16)
                elif action == 'passphrase':
                    self.output_text = self.pwd_gen.generate_passphrase()
                elif action == 'pin':
                    self.output_text = self.pwd_gen.generate_pin()
                elif action == 'analyze':
                    analysis = self.pwd_gen.analyze(self.input_text)
                    self.output_text = f"Strength: {analysis.strength.name}\nScore: {analysis.score}/5\nEntropy: {analysis.entropy:.1f} bits"
                self.message = f"✓ {action} completed"
        
        except Exception as e:
            self.output_text = f"Error: {str(e)}"
            self.message = "✗ Operation failed"
    
    def run(self):
        """Main TUI loop."""
        curses.curs_set(0)  # Hide cursor
        self.stdscr.clear()
        
        while True:
            self.stdscr.clear()
            self.draw_header()
            self.draw_input_section()
            self.draw_algorithm_selector()
            self.draw_key_input()
            self.draw_output_section()
            self.draw_help()
            self.stdscr.refresh()
            
            # Handle input
            try:
                key = self.stdscr.getch()
            except:
                break
            
            if key == ord('q') or key == ord('Q'):
                break
            elif key == ord('\t'):
                self.current_tab = (self.current_tab + 1) % len(self.tabs)
                self.selected_algo = 0
            elif key == curses.KEY_LEFT:
                self.selected_algo = max(0, self.selected_algo - 1)
            elif key == curses.KEY_RIGHT:
                self.selected_algo = min(len(self.algorithms[self.current_tab]) - 1, self.selected_algo + 1)
            elif key == curses.KEY_UP:
                self.current_tab = (self.current_tab - 1) % len(self.tabs)
                self.selected_algo = 0
            elif key == curses.KEY_DOWN:
                self.current_tab = (self.current_tab + 1) % len(self.tabs)
                self.selected_algo = 0
            elif key == ord('\n') or key == curses.KEY_ENTER:
                self.process_input()
            elif key == ord('c') or key == ord('C'):
                self.input_text = ""
                self.output_text = ""
                self.key_text = ""
                self.message = "Cleared"
            elif key == curses.KEY_BACKSPACE or key == 127:
                if self.current_tab == 2 and self.key_text:
                    self.key_text = self.key_text[:-1]
                else:
                    self.input_text = self.input_text[:-1]
            elif key == ord('k') or key == ord('K'):
                # Switch to key input mode for encryption
                if self.current_tab == 2:
                    # Next chars go to key
                    pass
            elif 32 <= key <= 126:  # Printable characters
                char = chr(key)
                if self.current_tab == 2 and self.key_text or char.isalnum():
                    # Simple heuristic: if key is being entered
                    self.input_text += char


def run_tui():
    """Run the TUI application."""
    def main(stdscr):
        tui = HashForgeTUI(stdscr)
        tui.run()
    
    curses.wrapper(main)


if __name__ == '__main__':
    run_tui()
