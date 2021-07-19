import matplotlib.pyplot as plt
import seaborn as sb
import spotifystats

# generates a pyplot for songs per artist in user's top 50 tracks
def plot_songs_per_artist(top50):
    # organizes by descending order of number of tracks per artist
    descending = top50['artist'].value_counts().sort_values(ascending=False).index
    ax = sb.countplot(y = top50['artist'], order=descending)

    sb.despine(fig=None, ax=None, top=True, right=True, left=False, trim=False)
    sb.set(rc={'figure.figsize':(6,7.2)})

    # set graph labels and titles
    ax.set_ylabel('artist')    
    ax.set_xlabel('number of songs')
    ax.set_title('Songs per artist in top 50 tracks', fontsize=13, fontweight='heavy')

    sb.set(font_scale = 1.4) # seaborn styling
    ax.axes.get_xaxis().set_visible(False)
    ax.set_frame_on(False)

    y = top50['artist'].value_counts()

    for i, v in enumerate(y):
        ax.text(v + 0.2, i + .16, str(v), color='black', fontweight='light', fontsize=14)
        
    plt.savefig('top50_tracks_per_artist.jpg', bbox_inches="tight")

if __name__ == "__main__":
    tracks = spotifystats.list_all_songs()
    top50 = tracks.to_csv('top50_tracks.csv')
    plot_songs_per_artist(top50)