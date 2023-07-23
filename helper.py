import matplotlib.pyplot as plt
from matplotlib import transforms

# matplotlib doesn't have a function for drawing text with
# different colors, let's implement it
def rainbow_text(x, y, text, colors, spacing=20, ax=None, **kw):
    colors = list(reversed(colors))
    t = ax.transData
    canvas = ax.figure.canvas

    for i, line in enumerate(reversed(text.split('\n'))):
        strings = line.split('||')
        for s, c in zip(strings, colors[i]):
            text = ax.text(x, y, s, color=c, transform=t, **kw)
            text.draw(canvas.get_renderer())
            ex = text.get_window_extent()
            t = transforms.offset_copy(text._transform, x=ex.width,
                                       units='dots')

        t = transforms.offset_copy(ax.transData, x=0, y=(i + 1) * spacing,
                                   units='dots')

def set_bar_pcnt(bar, val):
    plt.text(bar.get_x()+bar.get_width(), bar.get_y()+bar.get_height()-0.1,
             str(val)+'%  ',
             fontsize=10,
             horizontalalignment='right',
             color='white')