import matplotlib.pyplot as plt
import seaborn as sb
import spotifystats

def plot_songs_per_artist(top50):
    descending_order = top50['artist'].value_counts().sort_values(ascending=False).index
    ax = sb.countplot(y = top50['artist'], order=descending_order)

    sb.despine(fig=None, ax=None, top=True, right=True, left=False, trim=False)
    sb.set(rc={'figure.figsize':(6,7.2)})

    ax.set_ylabel('')    
    ax.set_xlabel('')
    ax.set_title('Songs per Artist in Top 50', fontsize=16, fontweight='heavy')
    sb.set(font_scale = 1.4)
    ax.axes.get_xaxis().set_visible(False)
    ax.set_frame_on(False)

    y = top50['artist'].value_counts()
    for i, v in enumerate(y):
        ax.text(v + 0.2, i + .16, str(v), color='black', fontweight='light', fontsize=14)
        
    plt.savefig('top50_songs_per_artist.jpg', bbox_inches="tight")

if __name__ == "__main__":
    spotify = spotifystats.SpotifyStats()
    tracks = spotify.list_all_songs()
    top50 = tracks.to_csv('top50_songs.csv')
    plot_songs_per_artist(top50)