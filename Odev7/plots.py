import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Agg')

def generate_plot():
    num_points = 1000
    x_coords = np.random.randint(0, 1000, size=num_points)
    y_coords = np.random.randint(0, 1000, size=num_points)

    df = pd.DataFrame({"x": x_coords, "y": y_coords})

    grid_size = 200

    colors = [
        "pink",
        "brown",
        "red",
        "black",
        "orange",
        "yellow",
        "blue",
        "gray",
        "purple",
        "green",
    ]

    plt.figure(figsize=(10, 10))

    color_index = 0

    for i in range(0, 1000, grid_size):
        for j in range(0, 1000, grid_size):
            mask = (
                (x_coords >= i)
                & (x_coords < i + grid_size)
                & (y_coords >= j)
                & (y_coords < j + grid_size)
            )

            color_index += 1
            
            if(color_index >= len(colors)):
                color_index = 0

            plt.scatter(x_coords[mask], y_coords[mask],
                        s=10, color=colors[color_index])

    plt.title("Rastgele Noktalar")
    plt.xlabel("X Koordinatları")
    plt.ylabel("Y Koordinatları")
    plt.grid(True)
    plt.savefig("./static/images/plot.jpg")
    print("Plot generated and saved to static/images/plot.jpg")
