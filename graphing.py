import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data from CSV file
file_path = '501200heat.csv'  # Replace with your CSV file path
data = pd.read_csv(file_path, index_col=0)

# Create the heatmap
plt.figure(figsize=(12, 8))
ax = sns.heatmap(data,
                 annot=True,           # Show values in cells
                 fmt='.1f',            # Format numbers to 4 decimal places
                 cmap='coolwarm',      # Color scheme
                 cbar_kws={'label': 'Średni czas wykonania [ms]'})

# Invert the y-axis to start with 100 at the bottom
ax.invert_yaxis()

# Customize the plot
# plt.title('Heatmap of CSV Data', fontsize=16, fontweight='bold')
plt.xlabel('Liczba klauzul', fontsize=12)
plt.ylabel('Liczba literałów', fontsize=12)

# Adjust layout to prevent label cutoff
plt.tight_layout()

# Display the plot
plt.show()

# Optional: Save the heatmap as an image file
# plt.savefig('heatmap.png', dpi=300, bbox_inches='tight')
