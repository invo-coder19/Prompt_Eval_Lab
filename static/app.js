// Prompt Evaluation Platform - Frontend Logic

class PromptEvaluator {
    constructor() {
        this.selectedPrompts = new Set();
        this.init();
    }

    init() {
        this.loadPrompts();
        this.setupEventListeners();
        this.loadLeaderboard();
    }

    /**
     * Show a toast notification
     * @param {string} message - Message to display
     * @param {string} type - Type: 'success', 'error', 'warning', 'info'
     * @param {number} duration - How long to show (ms), 0 for permanent
     */
    showToast(message, type = 'info', duration = 5000) {
        const container = document.getElementById('toastContainer');
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;

        const icons = {
            success: '✓',
            error: '✕',
            warning: '⚠',
            info: 'ℹ'
        };

        const titles = {
            success: 'Success',
            error: 'Error',
            warning: 'Warning',
            info: 'Info'
        };

        toast.innerHTML = `
            <span class="toast-icon">${icons[type] || icons.info}</span>
            <div class="toast-content">
                <div class="toast-title">${titles[type] || titles.info}</div>
                <div class="toast-message">${message}</div>
            </div>
            <button class="toast-close" aria-label="Close">&times;</button>
        `;

        container.appendChild(toast);

        // Close button functionality
        const closeBtn = toast.querySelector('.toast-close');
        closeBtn.addEventListener('click', () => {
            this.removeToast(toast);
        });

        // Auto-remove after duration
        if (duration > 0) {
            setTimeout(() => {
                this.removeToast(toast);
            }, duration);
        }

        return toast;
    }

    removeToast(toast) {
        toast.classList.add('hiding');
        setTimeout(() => {
            toast.remove();
        }, 300); // Match animation duration
    }


    setupEventListeners() {
        const runBtn = document.getElementById('runEvalBtn');
        runBtn.addEventListener('click', () => this.runEvaluation());
    }

    async loadPrompts() {
        const promptList = document.getElementById('promptList');

        try {
            const response = await fetch('/api/prompts');
            const prompts = await response.json();

            if (prompts.length === 0) {
                promptList.innerHTML = '<div class="loading">No prompts found</div>';
                return;
            }

            promptList.innerHTML = '';

            prompts.forEach(prompt => {
                const item = this.createPromptItem(prompt);
                promptList.appendChild(item);
            });

        } catch (error) {
            console.error('Error loading prompts:', error);
            promptList.innerHTML = '<div class="loading">Error loading prompts</div>';
        }
    }

    createPromptItem(promptName) {
        const div = document.createElement('div');
        div.className = 'prompt-item';

        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.id = `prompt-${promptName}`;
        checkbox.value = promptName;
        checkbox.addEventListener('change', (e) => this.handlePromptSelection(e));

        const label = document.createElement('label');
        label.htmlFor = `prompt-${promptName}`;
        label.textContent = promptName;

        div.appendChild(checkbox);
        div.appendChild(label);

        return div;
    }

    handlePromptSelection(event) {
        const promptName = event.target.value;

        if (event.target.checked) {
            this.selectedPrompts.add(promptName);
        } else {
            this.selectedPrompts.delete(promptName);
        }

        // Enable/disable run button
        const runBtn = document.getElementById('runEvalBtn');
        runBtn.disabled = this.selectedPrompts.size === 0;
    }

    async runEvaluation() {
        if (this.selectedPrompts.size === 0) {
            return;
        }

        const overlay = document.getElementById('loadingOverlay');
        overlay.classList.remove('hidden');

        try {
            const response = await fetch('/api/evaluate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    prompts: Array.from(this.selectedPrompts)
                })
            });

            const result = await response.json();

            if (result.success) {
                this.displayLeaderboard(result.leaderboard);
                this.updateTimestamp();
                this.showToast('Evaluation completed successfully!', 'success');
            } else {
                this.showToast(result.error || 'Evaluation failed', 'error');
            }

        } catch (error) {
            console.error('Error running evaluation:', error);
            this.showToast('Failed to run evaluation. Please try again.', 'error');
        } finally {
            overlay.classList.add('hidden');
        }
    }

    async loadLeaderboard() {
        try {
            const response = await fetch('/api/leaderboard');
            const leaderboard = await response.json();

            if (!leaderboard.error && leaderboard.length > 0) {
                this.displayLeaderboard(leaderboard);
                this.updateTimestamp();
            }
        } catch (error) {
            // Leaderboard doesn't exist yet, that's okay
            console.log('No existing leaderboard');
        }
    }

    displayLeaderboard(data) {
        const content = document.getElementById('leaderboardContent');

        if (!data || data.length === 0) {
            content.innerHTML = `
                <div class="empty-state">
                    <svg class="empty-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <path d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    <p>No evaluation results yet. Select prompts and run evaluation.</p>
                </div>
            `;
            return;
        }

        const table = document.createElement('table');
        table.className = 'leaderboard-table';

        // Table header
        table.innerHTML = `
            <thead>
                <tr>
                    <th>Rank</th>
                    <th>Prompt</th>
                    <th>Overall</th>
                    <th>Similarity</th>
                    <th>Accuracy</th>
                    <th>Faithfulness</th>
                    <th>F1 Score</th>
                </tr>
            </thead>
            <tbody></tbody>
        `;

        const tbody = table.querySelector('tbody');

        data.forEach(entry => {
            const row = this.createLeaderboardRow(entry);
            tbody.appendChild(row);
        });

        content.innerHTML = '';
        content.appendChild(table);
    }

    createLeaderboardRow(entry) {
        const tr = document.createElement('tr');

        // Rank badge
        const rankClass = entry.rank <= 3 ? `rank-${entry.rank}` : 'rank-other';

        tr.innerHTML = `
            <td>
                <span class="rank-badge ${rankClass}">${entry.rank}</span>
            </td>
            <td><strong>${entry.prompt_name}</strong></td>
            <td>${this.formatScore(entry.overall_score)}</td>
            <td>${this.formatScore(entry.semantic_similarity)}</td>
            <td>${this.formatScore(entry.accuracy)}</td>
            <td>${this.formatScore(entry.faithfulness)}</td>
            <td>${this.formatScore(entry.f1_score)}</td>
        `;

        return tr;
    }

    formatScore(score) {
        const value = (score * 100).toFixed(1);
        let scoreClass = 'score-low';

        if (score >= 0.8) {
            scoreClass = 'score-high';
        } else if (score >= 0.6) {
            scoreClass = 'score-medium';
        }

        return `<span class="score ${scoreClass}">${value}%</span>`;
    }

    updateTimestamp() {
        const timestampEl = document.getElementById('lastUpdated');
        const now = new Date();
        const timeStr = now.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit'
        });
        timestampEl.textContent = `Last updated: ${timeStr}`;
    }
}

// Initialize the app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new PromptEvaluator();
});
