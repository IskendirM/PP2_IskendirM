import pygame
import os
import time

pygame.mixer.init()

class MusicPlayer:
    def __init__(self):
        self.is_playing = False
        self.current_song_index = 0
        self.songs = self.load_songs("C:/Users/Lenovo/Desktop/PP2_IskendirM/Lab 7/muson")
        self.current_song = None

    def load_songs(self, folder):
        """Load all the song files from a given folder."""
        songs = []
        for file in os.listdir(folder):
            if file.endswith(".mp3"):
                songs.append(os.path.join(folder, file))
        return songs

    def play(self):
        """Play the current song."""
        if self.songs:
            pygame.mixer.music.load(self.songs[self.current_song_index])
            pygame.mixer.music.play()
            self.is_playing = True
            print(f"Playing: {os.path.basename(self.songs[self.current_song_index])}")

    def stop(self):
        """Stop the music."""
        pygame.mixer.music.stop()
        self.is_playing = False
        print("Music stopped.")

    def next_song(self):
        """Skip to the next song."""
        if self.songs:
            self.current_song_index = (self.current_song_index + 1) % len(self.songs)
            if self.is_playing:
                self.play()
            else:
                print(f"Next song: {os.path.basename(self.songs[self.current_song_index])}")

    def previous_song(self):
        """Go to the previous song."""
        if self.songs:
            self.current_song_index = (self.current_song_index - 1) % len(self.songs)
            if self.is_playing:
                self.play()
            else:
                print(f"Previous song: {os.path.basename(self.songs[self.current_song_index])}")


def main():
    player = MusicPlayer()

    pygame.display.set_mode((1, 1)) 

    print("Music Player Controls:")
    print("Press 'p' to Play, 's' to Stop, 'n' for Next, 'b' for Previous, 'q' to Quit.")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p: 
                    if not player.is_playing:
                        player.play()
                    else:
                        print("Music is already playing.")
                
                elif event.key == pygame.K_s: 
                    player.stop()
                
                elif event.key == pygame.K_n: 
                    player.next_song()
                
                elif event.key == pygame.K_b:
                    player.previous_song()
                
                elif event.key == pygame.K_q:
                    print("Quitting...")
                    pygame.quit()
                    return

        time.sleep(0.1)

if __name__ == "__main__":
    main()
    







