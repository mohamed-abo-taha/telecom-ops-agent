"""Assistant architecture diagram -> assets/architecture.png."""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fig, ax = plt.subplots(figsize=(12.5, 3.0))
ax.set_xlim(0, 12.5)
ax.set_ylim(0, 3.0)
ax.axis('off')

boxes = [
    (0.2, 'User\nquestion', '#e3f2fd'),
    (2.6, 'LLM router\n(JSON mode,\nLlama-3.2)', '#f3e5f5'),
    (5.2, 'Tools (code)\nlookup_customer,\nplan, roaming', '#fff3e0'),
    (7.9, 'Tool results\n(grounded facts)', '#e8f5e9'),
    (10.3, 'LLM writes\nfinal answer', '#f3e5f5'),
]
w, h, y = 2.1, 1.5, 0.75
for x, label, color in boxes:
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.05', fc=color, ec='#555'))
    ax.text(x + w / 2, y + h / 2, label, ha='center', va='center', fontsize=8.5)
for i in range(len(boxes) - 1):
    ax.add_patch(FancyArrowPatch((boxes[i][0] + w, y + h / 2), (boxes[i + 1][0], y + h / 2),
                                 arrowstyle='->', mutation_scale=15, color='#333'))
ax.text(6.25, 2.7, 'Telecom ops assistant (FastAPI, fully local via Ollama)', ha='center', fontsize=12, weight='bold')
ax.text(6.25, 0.3, 'POST /ask  ->  { answer, trace[] }   (tools run in code, so the answer is grounded)',
        ha='center', fontsize=8.5, color='#444')

os.makedirs(os.path.join(root, 'assets'), exist_ok=True)
plt.tight_layout()
plt.savefig(os.path.join(root, 'assets', 'architecture.png'), dpi=130, bbox_inches='tight')
print('wrote assets/architecture.png')
