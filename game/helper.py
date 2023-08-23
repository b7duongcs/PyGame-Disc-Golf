import matplotlib.pyplot as plt
from IPython import display

plt.ion()

def plot(distances, mean_distance):
    display.clear_output(wait=True)
    display.display(plt.gcf())
    plt.clf()
    plt.title('Training...')
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(distances)
    plt.plot(mean_distance)
    plt.ylim(ymin=0)
    plt.text(len(distances)-1, distances[-1], str(distances[-1]))
    plt.text(len(mean_distance)-1, mean_distance[-1], str(mean_distance[-1]))
    plt.show(block=False)
    plt.pause(.1)