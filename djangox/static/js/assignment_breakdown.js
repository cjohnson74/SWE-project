function debugLog(message, data = null) {
    if (!DEBUG) return;
    
    const timestamp = new Date().toISOString();
    console.log(`[${timestamp}] ${message}`);
    if (data) {
        console.log('Data:', data);
    }
}

// Hide debug section if DEBUG is false
document.addEventListener('DOMContentLoaded', function() {
    if (!DEBUG) {
        const debugSection = document.querySelector('.debug-section');
        if (debugSection) {
            debugSection.style.display = 'none'; // Hide the debug section
        }
    }
});

// Define updateTaskProgress before using it
function updateTaskProgress() {
    debugLog('Updating task progress');
    
    const checkboxes = document.querySelectorAll('.task-checkbox');
    let completedCount = 0;
    const totalCount = checkboxes.length;

    debugLog('Found checkboxes', {
        total: totalCount,
        checkboxes: Array.from(checkboxes).map(cb => ({
            completed: cb.dataset.completed,
            checked: cb.checked
        }))
    });

    checkboxes.forEach(checkbox => {
        const isCompleted = checkbox.dataset.completed === 'true';
        if (isCompleted) {
            completedCount++;
        }
    });

    const progressPercentage = (completedCount / totalCount) * 100;
    debugLog('Progress calculation', {
        completed: completedCount,
        total: totalCount,
        percentage: progressPercentage
    });
    
    // Update progress bar
    const progressBar = document.getElementById('progressFill');
    progressBar.style.width = `${progressPercentage}%`;
    progressBar.setAttribute('aria-valuenow', progressPercentage);

    // Update progress message
    document.getElementById('completedCount').textContent = completedCount;
    document.getElementById('totalCount').textContent = totalCount;

    // Trigger confetti if all tasks are completed
    if (completedCount === totalCount) {
        debugLog('All tasks completed, triggering celebration');
        confetti({
            particleCount: 100,
            spread: 70,
            origin: { y: 0.6 }
        });
    }
}

function createTaskCard(task) {
    // Convert arrays to lists if they're strings
    const distractions = typeof task.potential_distractions === 'string' ? 
        task.potential_distractions.split(',').filter(Boolean) : 
        task.potential_distractions || [];
    
    const focusTechniques = typeof task.focus_techniques === 'string' ? 
        task.focus_techniques.split(',').filter(Boolean) : 
        task.focus_techniques || [];

    return `
        <div class="task-card ${task.completed ? 'completed' : ''} animate__animated animate__fadeIn">
            <div class="task-header" onclick="toggleTaskDetails(this)">
                <div class="task-main-content">
                    <div class="checkbox-wrapper">
                        <input type="checkbox" 
                               class="task-checkbox" 
                               onchange="updateProgress()" 
                               data-task-number="${task.task_number}"
                               ${task.completed ? 'checked' : ''}>
                    </div>
                    <div class="task-title">
                        <h4 class="mb-0">
                            <span class="task-number">Task ${task.task_number }:</span>
                            ${task.description}
                        </h4>
                    </div>
                </div>
                <div class="task-meta">
                    <span class="meta-item estimated-time">
                        <i class="far fa-clock"></i> ${task.estimated_time}
                    </span>
                    ${task.due_date ? `
                        <span class="meta-item due-date" data-date="${task.due_date}">
                            <i class="far fa-calendar-alt"></i> 
                            ${new Date(task.due_date).toLocaleString('en-US', {
                                weekday: 'long',
                                year: 'numeric',
                                month: 'long',
                                day: 'numeric',
                                hour: 'numeric',
                                minute: 'numeric'
                            })}
                        </span>
                    ` : ''}
                    ${task.priority ? `
                        <span class="meta-item priority-badge ${task.priority.toLowerCase()}">
                            <i class="fas fa-flag"></i> ${task.priority}
                        </span>
                    ` : ''}
                </div>
            </div>
            <div class="task-details" style="display: none;">
                <div class="details-grid">
                    ${task.tips ? `
                        <div class="detail-section tips-section">
                            <div class="section-header">
                                <i class="fas fa-lightbulb"></i>
                                <h5>Tips</h5>
                            </div>
                            <p>${task.tips}</p>
                        </div>
                    ` : ''}
                    
                    ${distractions.length > 0 ? `
                        <div class="detail-section distractions-section">
                            <div class="section-header">
                                <i class="fas fa-exclamation-triangle"></i>
                                <h5>Potential Distractions</h5>
                            </div>
                            <ul class="distraction-list">
                                ${distractions.map(d => `<li>${d.trim()}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}

                    ${task.distraction_mitigation ? `
                        <div class="detail-section mitigation-section">
                            <div class="section-header">
                                <i class="fas fa-shield-alt"></i>
                                <h5>Distraction Mitigation</h5>
                            </div>
                            <p>${task.distraction_mitigation}</p>
                        </div>
                    ` : ''}

                    ${focusTechniques.length > 0 ? `
                        <div class="detail-section techniques-section">
                            <div class="section-header">
                                <i class="fas fa-bullseye"></i>
                                <h5>Focus Techniques</h5>
                            </div>
                            <ul class="technique-list">
                                ${focusTechniques.map(t => `<li>${t.trim()}</li>`).join('')}
                            </ul>
                        </div>
                    ` : ''}

                    ${task.reward ? `
                        <div class="detail-section reward-section">
                            <div class="section-header">
                                <i class="fas fa-gift"></i>
                                <h5>Reward</h5>
                            </div>
                            <p>${task.reward}</p>
                        </div>
                    ` : ''}
                    
                    ${task.youtube_resources && task.youtube_resources.length > 0 ? `
                        <div class="detail-section video-section">
                            <div class="section-header">
                                <i class="fab fa-youtube"></i>
                                <h5>Helpful Videos</h5>
                            </div>
                            <div class="video-grid">
                                ${task.youtube_resources.map(resource => `
                                    <div class="video-card">
                                        <a href="${resource.link}" 
                                           target="_blank" 
                                           rel="noopener noreferrer"
                                           class="video-link">
                                            <div class="video-thumbnail">
                                                <i class="fab fa-youtube"></i>
                                                <span class="play-icon">
                                                    <i class="fas fa-play-circle"></i>
                                                </span>
                                            </div>
                                            <div class="video-title">
                                                ${resource.title}
                                            </div>
                                        </a>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    ` : ''}
                </div>
            </div>
        </div>
    `;
}

// Define loading configuration
const LOADING_CONFIG = {
    AVERAGE_TIME: 15000, // 15 seconds total
    STEPS: [
        { percent: 10, message: "🤔 Analyzing assignment..." },
        { percent: 25, message: "📚 Breaking down requirements..." },
        { percent: 40, message: "⚡ Identifying potential challenges..." },
        { percent: 55, message: "📋 Creating task list..." },
        { percent: 70, message: "⏱️ Estimating time requirements..." },
        { percent: 85, message: "🎯 Finalizing breakdown..." },
        { percent: 95, message: "✨ Almost there..." }
    ]
};

function simulateProgress() {
    let currentStep = 0;
    const progressBar = document.getElementById('loadingProgress');
    const loadingTitle = document.querySelector('.loading-title');
    
    if (!progressBar || !loadingTitle) {
        console.error('Progress elements not found:', { progressBar, loadingTitle });
        return;
    }

    // Reset progress
    progressBar.style.width = '0%';
    progressBar.setAttribute('aria-valuenow', 0);
    loadingTitle.textContent = LOADING_CONFIG.STEPS[0].message;

    function animateToPercent(fromPercent, toPercent, duration) {
        const startTime = performance.now();
        
        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            const currentPercent = fromPercent + (toPercent - fromPercent) * progress;
            progressBar.style.width = `${currentPercent}%`;
            progressBar.setAttribute('aria-valuenow', Math.round(currentPercent));

            if (progress < 1) {
                requestAnimationFrame(update);
            }
        }

        requestAnimationFrame(update);
    }

    function nextStep() {
        if (currentStep >= LOADING_CONFIG.STEPS.length) return;

        const currentPercent = currentStep > 0 ? LOADING_CONFIG.STEPS[currentStep - 1].percent : 0;
        const targetPercent = LOADING_CONFIG.STEPS[currentStep].percent;
        const stepDuration = LOADING_CONFIG.AVERAGE_TIME / LOADING_CONFIG.STEPS.length;

        // Update message
        loadingTitle.textContent = LOADING_CONFIG.STEPS[currentStep].message;
        
        // Animate progress bar to next percentage
        animateToPercent(currentPercent, targetPercent, stepDuration);

        currentStep++;

        // Schedule next step if not at end
        if (currentStep < LOADING_CONFIG.STEPS.length) {
            setTimeout(nextStep, stepDuration);
        } else {
            // Final animation to 100%
            setTimeout(() => {
                animateToPercent(targetPercent, 100, 1000);
                loadingTitle.textContent = '✅ Analysis complete!';
            }, stepDuration);
        }
    }

    // Start the progress animation
    nextStep();
}

// Add some CSS for better visualization
const style = document.createElement('style');
style.textContent = `
    .loading-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(255, 255, 255, 0.9);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
    }

    .loading-container {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
        max-width: 600px;
        width: 90%;
    }

    .loading-content {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .progress {
        width: 100%;
        height: 25px;
        background-color: #e9ecef;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: inset 0 1px 2px rgba(0,0,0,0.1);
    }

    .progress-bar {
        background-color: #007bff;
        transition: width 0.5s ease-in-out;
    }

    .loading-title {
        color: #2c3e50;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
    }
`;
document.head.appendChild(style);

async function submitForm(event) {
    event.preventDefault();
    debugLog('Form submitted');

    const loadingElement = document.getElementById('loading');
    const formElement = document.getElementById('breakdownForm');
    const resultsElement = document.getElementById('breakdownResults');

    try {
        // Show loading state
        if (loadingElement && formElement && resultsElement) {
            formElement.style.display = 'none';
            loadingElement.style.display = 'block';
            resultsElement.style.display = 'none';
        }

        // Start progress animation
        simulateProgress();

        // Get form data
        const form = event.target;
        const formData = new FormData(form);
        const assignment_id = formData.get('assignment_id');

        // Make the API call
        const response = await fetch(form.action, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                assignment_id: assignment_id
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || `Error getting breakdown: ${response.status}`);
        }

        const data = await response.json();
        debugLog('Received response:', data);

        if (data.status === 'success') {
            window.location.reload();
            // // Hide loading and show results
            // if (loadingElement && resultsElement) {
            //     loadingElement.style.display = 'none';
            //     resultsElement.style.display = 'block';
                
            // }

            // Update the task list and next task
            if (data.tasks) {
                updateTaskList(data.tasks);
                updateNextTask(data.tasks);
            }
        } else {
            throw new Error(data.message || 'Failed to get assignment breakdown');
        }
    } catch (error) {
        console.error('Error:', error);
        const errorMessage = document.getElementById('noBreakdownMessage');
        if (errorMessage) {
            errorMessage.style.display = 'block';
            errorMessage.textContent = `Error: ${error.message}`;
        }
        // Show form again on error
        if (formElement) {
            formElement.style.display = 'block';
        }
    } finally {
        // Hide loading spinner after a delay to ensure progress animation completes
        setTimeout(() => {
            if (loadingElement) {
                loadingElement.style.display = 'none';
            }
        }, 1000);
    }
}
// Add event listener for when the page is hidden/shown
// Add event listener for when the page is hidden/shown
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        simulateProgress();
    }
});

function updateNextTask(tasks) {
    const nextIncompleteTask = tasks.find(task => !task.completed);
    const nextTaskContent = document.getElementById('nextTaskContent');
    
    if (!nextTaskContent) return;

    if (nextIncompleteTask) {
        nextTaskContent.innerHTML = `
            <div class="task-card priority-high animate__animated animate__fadeIn">
                <div class="task-header">
                    <h4 class="mb-3">
                        <i class="fas fa-star text-warning"></i> 
                        Task ${nextIncompleteTask.task_number }: ${nextIncompleteTask.description}
                    </h4>
                </div>
                <div class="task-details">
                    <div class="row">
                        <div class="col-md-6">
                            <p><i class="far fa-clock"></i> <strong>Estimated Time:</strong> ${nextIncompleteTask.estimated_time}</p>
                            <p><i class="far fa-calendar-alt"></i> <strong>Due Date:</strong> ${
                                new Date(nextIncompleteTask.due_date).toLocaleString('en-US', {
                                    year: 'numeric',
                                    month: 'long',
                                    day: 'numeric',
                                    hour: 'numeric',
                                    minute: 'numeric'
                                })
                            }</p>
                        </div>
                        <div class="col-md-6">
                            ${nextIncompleteTask.tips ? `
                                <div class="alert alert-info">
                                    <i class="fas fa-lightbulb"></i> <strong>Tips:</strong><br>
                                    ${nextIncompleteTask.tips}
                                </div>
                            ` : ''}
                        </div>
                    </div>
                    
                    ${nextIncompleteTask.youtube_resources && nextIncompleteTask.youtube_resources.length > 0 ? `
                        <div class="resources mt-3">
                            <h5><i class="fab fa-youtube text-danger"></i> Helpful Resources:</h5>
                            <div class="list-group">
                                ${nextIncompleteTask.youtube_resources.map(resource => `
                                    <a href="${resource.link}" 
                                       target="_blank" 
                                       class="list-group-item list-group-item-action">
                                        <i class="fas fa-play-circle"></i> ${resource.title}
                                    </a>
                                `).join('')}
                            </div>
                        </div>
                    ` : ''}
                </div>
            </div>
        `;
    } else {
        nextTaskContent.innerHTML = `
            <div class="alert alert-success text-center">
                <i class="fas fa-check-circle fa-2x mb-2"></i>
                <h4>All Caught Up!</h4>
                <p>No upcoming tasks. Great job staying on top of your work!</p>
            </div>
        `;
    }
}

function getTaskDataFromElement(taskCard) {
    // Helper function to extract task data from DOM element
    return {
        description: taskCard.querySelector('.task-header').textContent.trim(),
        estimated_time: taskCard.querySelector('.estimated-time')?.textContent.trim(),
        due_date: taskCard.querySelector('.due-date')?.dataset.date,
        tips: taskCard.querySelector('.task-details')?.querySelector('em:contains("Tips:")')?.nextSibling?.textContent.trim(),
        youtube_resources: Array.from(taskCard.querySelectorAll('.task-details a')).map(a => ({
            link: a.href,
            title: a.textContent.trim()
        }))
    };
}

// Initialize after all functions are defined
document.addEventListener('DOMContentLoaded', function() {
    debugLog('Page loaded, initializing...');
    debugLog('Has existing breakdown:', hasExistingBreakdown);
    
    if (hasExistingBreakdown) {
        debugLog('Showing existing breakdown');
        document.getElementById('breakdownResults').style.display = 'block';
        updateTaskProgress();
    } else {
        debugLog('No existing breakdown, showing form');
    }
});

// Function to play a celebratory sound
function playCelebrationSound() {
    const audio = new Audio('{% static "sounds/celebration.mp3" %}'); // Ensure you have a sound file in your static directory
    audio.play();
}

function showLoading() {
    document.getElementById('loading').style.display = 'flex'; // Show loading visual
    document.getElementById('breakdownForm').style.display = 'none'; // Hide the form
    document.querySelector('.container').style.backgroundColor = '#2c3e50'; // Dark background for focus
    document.querySelector('.container').style.color = 'white'; // White text for contrast

    // Reset loading progress
    const loadingProgress = document.getElementById('loadingProgress');
    loadingProgress.style.width = '0%';
    loadingProgress.setAttribute('aria-valuenow', 0);
}

function hideLoading() {
    document.getElementById('loading').style.display = 'none'; // Hide loading spinner
    document.getElementById('breakdownForm').style.display = 'block'; // Show the form again
    document.querySelector('.container').style.backgroundColor = ''; // Reset container background color
    document.querySelector('.container').style.color = ''; // Reset container text color
}

function updateLoadingProgress(percentage) {
    const loadingProgress = document.getElementById('loadingProgress');
    loadingProgress.style.width = `${percentage}%`;
    loadingProgress.setAttribute('aria-valuenow', percentage);
}

function toggleSection(header) {
    const content = header.nextElementSibling;
    content.style.display = content.style.display === 'none' ? 'block' : 'none';
    header.querySelector('.arrow').textContent = content.style.display === 'block' ? '▲' : '▼';
}

function toggleTaskDetails(header) {
    const details = header.nextElementSibling;
    details.style.display = details.style.display === 'none' ? 'block' : 'none';
}

function getBorderColor(estimatedTime) {
    const timeRange = estimatedTime.split('-').map(t => parseInt(t));
    const averageTime = (timeRange.length === 2) ? (timeRange[0] + timeRange[1]) / 2 : timeRange[0];
    
    if (averageTime <= 30) return '#2ecc71'; // Green for short tasks
    if (averageTime <= 60) return '#f1c40f'; // Yellow for medium tasks
    return '#e74c3c'; // Red for long tasks
}

function findNextIncompleteTask() {
    const taskCards = document.querySelectorAll('.task-card');
    for (const taskCard of taskCards) {
        const checkbox = taskCard.querySelector('.task-checkbox');
        if (!checkbox.checked) {
            return {
                taskNumber: checkbox.dataset.taskNumber,
                description: taskCard.querySelector('strong').nextSibling.textContent.trim(),
                estimatedTime: taskCard.querySelector('.estimated-time').textContent.trim(),
                dueDate: taskCard.querySelector('.due-date')?.querySelector('script')?.textContent
            };
        }
    }
    return null;
}

function updateNextTaskDisplay(nextTask) {
    const nextTaskSection = document.querySelector('.next-task-card');
    
    if (!nextTask) {
        // If no next task, hide or update the section accordingly
        if (nextTaskSection) {
            nextTaskSection.innerHTML = `
                <h4><i class="fas fa-check-circle text-success"></i> All Tasks Completed!</h4>
                <div class="card">
                    <div class="card-body">
                        <p class="card-text text-success">
                            
            `;
        }
    } else {
        // If there's a next task, update the section accordingly
        nextTaskSection.innerHTML = `
            <div class="task-card priority-high animate__animated animate__fadeIn">
                <div class="task-header">
                    <h4 class="mb-3">
                        <i class="fas fa-star text-warning"></i> 
                        Task ${nextTask.taskNumber}: ${nextTask.description}
                    </h4>
                </div>
                <div class="task-details">
                    <div class="row">
                        <div class="col-md-6">
                            <p><i class="far fa-clock"></i> <strong>Estimated Time:</strong> ${nextTask.estimatedTime}</p>
                            <p><i class="far fa-calendar-alt"></i> <strong>Due Date:</strong> ${nextTask.dueDate}</p>
                        </div>
                        <div class="col-md-6">
                            ${nextTask.tips ? `<div class="alert alert-info">
                                <i class="fas fa-lightbulb"></i> <strong>Tips:</strong><br>
                                ${nextTask.tips}
                            </div>` : ''}
                        </div>
                    </div>
                    
                    ${nextTask.youtubeResources ? `<div class="resources mt-3">
                        <h5><i class="fab fa-youtube text-danger"></i> Helpful Resources:</h5>
                        <div class="list-group">
                            ${nextTask.youtubeResources.map(resource => `<a href="${resource.link}" target="_blank" class="list-group-item list-group-item-action">
                                <i class="fas fa-play-circle"></i> ${resource.title}
                            </a>`).join('')}
                        </div>
                    </div>` : ''}
                
                </div>
            </div>
        `;
    }
}

function saveProgress(completedCount, totalCount) {
    const assignmentId = getAssignmentIdFromUrl();
    fetch(`/api/save-progress/${assignmentId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify({
            completed_count: completedCount,
            total_count: totalCount,
            assignment_id: assignmentId
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Progress saved:', data);
    })
    .catch(error => {
        console.error('Error saving progress:', error);
    });
}

function markTaskComplete(taskNumber) {
    const checkbox = document.querySelector(`.task-checkbox[data-task-number="${taskNumber}"]`);
    if (checkbox) {
        checkbox.checked = true;
        updateProgress();
    }
}

// Initialize progress on page load
document.addEventListener('DOMContentLoaded', function() {
    updateProgress();
});

// Add event listeners to all checkboxes
document.querySelectorAll('.task-checkbox').forEach(checkbox => {
    checkbox.addEventListener('change', updateProgress);
});

async function markTaskComplete(taskNumber) {
    const checkbox = document.querySelector(`.task-checkbox[data-task-number="${taskNumber}"]`);
    if (checkbox) {
        checkbox.checked = true;
        
        try {
            // Get assignment ID from URL
            const assignmentId = getAssignmentIdFromUrl();
            if (!assignmentId) {
                console.error('No assignment ID found');
                return;
            }
            // Save task completion status
            const response = await fetch(`/api/save-task-status/${taskNumber}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({
                    completed: true,
                    assignment_id: assignmentId
                })
            });

            if (!response.ok) {
                throw new Error('Failed to save task status');
            }

            // Update progress only if save was successful
            updateProgress();
            
            // Add visual feedback
            const taskCard = checkbox.closest('.task-card');
            if (taskCard) {
                taskCard.classList.add('completed');
                taskCard.classList.add('animate__animated', 'animate__fadeIn');
            }

        } catch (error) {
            console.error('Error saving task status:', error);
            checkbox.checked = false;
            alert('Failed to save task completion. Please try again.');
        }
    }
}

// Add event listener for checkbox changes
document.querySelectorAll('.task-checkbox').forEach(checkbox => {
    checkbox.addEventListener('change', async function(event) {
        const taskNumber = this.dataset.taskNumber;
        const isCompleted = this.checked;
        
        try {
            // Get assignment ID from URL
            const assignmentId = getAssignmentIdFromUrl();
            if (!assignmentId) {
                console.error('No assignment ID found');
                return;
            }
            const response = await fetch(`/api/save-task-status/${taskNumber}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({
                    completed: isCompleted,
                    assignment_id: assignmentId
                })
            });

            if (!response.ok) {
                throw new Error('Failed to save task status');
            }

            updateProgress();
            
            // Add visual feedback
            const taskCard = this.closest('.task-card');
            if (taskCard) {
                if (isCompleted) {
                    taskCard.classList.add('completed');
                } else {
                    taskCard.classList.remove('completed');
                }
            }

        } catch (error) {
            console.error('Error saving task status:', error);
            this.checked = !isCompleted;
            alert('Failed to save task completion. Please try again.');
        }
    });
});

// Add this function to handle task detail toggling
function toggleTaskDetails(element) {
    // Find the details div that follows the header
    const detailsDiv = element.nextElementSibling;
    if (!detailsDiv || !detailsDiv.classList.contains('task-details')) {
        return; // Exit if no details div found
    }

    // Toggle the display
    if (detailsDiv.style.display === 'none' || !detailsDiv.style.display) {
        detailsDiv.style.display = 'block';
        // Add animation class
        detailsDiv.classList.add('animate__animated', 'animate__fadeIn');
    } else {
        detailsDiv.style.display = 'none';
        // Remove animation classes
        detailsDiv.classList.remove('animate__animated', 'animate__fadeIn');
    }

    // Toggle arrow direction if it exists
    const arrow = element.querySelector('.arrow');
    if (arrow) {
        arrow.style.transform = detailsDiv.style.display === 'block' ? 'rotate(180deg)' : 'rotate(0deg)';
    }
}

function updateTaskList(tasks) {
    const taskList = document.getElementById('taskList');
    if (!taskList) {
        console.error('Task list container not found');
        return;
    }

    taskList.innerHTML = tasks.map(task => createTaskCard(task)).join('');
    
    // Add event listeners to new checkboxes
    taskList.querySelectorAll('.task-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            const taskCard = checkbox.closest('.task-card');
            if (taskCard) {
                if (checkbox.checked) {
                    taskCard.classList.add('completed');
                } else {
                    taskCard.classList.remove('completed');
                }
            }
            updateProgress();
        });
    });

    // Initialize progress
    updateProgress();
}

// Function to get assignment ID from URL
function getAssignmentIdFromUrl() {
    // URL pattern: /assignments/{assignment_id}/breakdown/
    const pathParts = window.location.pathname.split('/');
    const assignmentIdIndex = pathParts.indexOf('assignments') + 1;
    if (assignmentIdIndex > 0 && assignmentIdIndex < pathParts.length) {
        return pathParts[assignmentIdIndex];
    }
    console.error('Could not find assignment ID in URL');
    return null;
}

// Function to get CSRF token
function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]')?.value;
}

// Updated progress function
async function updateProgress() {
    const checkboxes = document.querySelectorAll('.task-checkbox');
    let completedCount = 0;
    const totalCount = checkboxes.length;

    // Count completed tasks
    checkboxes.forEach(checkbox => {
        if (checkbox.checked) completedCount++;
    });

    // Update progress bar
    const progressBar = document.getElementById('progressFill');
    if (progressBar) {
        const progressPercentage = (completedCount / totalCount) * 100;
        progressBar.style.width = `${progressPercentage}%`;
        progressBar.setAttribute('aria-valuenow', progressPercentage);
    }

    // Update progress message
    const completedElement = document.getElementById('completedCount');
    const totalElement = document.getElementById('totalCount');
    if (completedElement) completedElement.textContent = completedCount;
    if (totalElement) totalElement.textContent = totalCount;

    // Get assignment ID from URL
    const assignment_id = getAssignmentIdFromUrl();
    if (!assignment_id) {
        console.error('No assignment ID found');
        return;
    }

    // Get CSRF token
    const csrfToken = getCsrfToken();
    if (!csrfToken) {
        console.error('No CSRF token found');
        return;
    }

    // Save to backend
    try {
        const response = await fetch(`/api/save-progress/${assignment_id}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                completed_count: completedCount,
                total_count: totalCount,
                assignment_id: assignment_id
            })
        });

        const data = await response.json();
        
        if (data.status === 'success') {
            // Show confetti for 100% completion
            if (completedCount === totalCount) {
                confetti({
                    particleCount: 100,
                    spread: 70,
                    origin: { y: 0.6 }
                });
            }
        } else {
            console.error('Error saving progress:', data.message);
        }
    } catch (error) {
        console.error('Error updating progress:', error);
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Initial progress update
    updateProgress();
    
    // Add event listeners to checkboxes
    document.querySelectorAll('.task-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', updateProgress);
    });
});

function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();
    
    const dt = e.dataTransfer;
    const files = dt.files;
    handleFiles(files);
    document.getElementById('dropZone').classList.remove('dragover');
}

function handleDragOver(e) {
    e.preventDefault();
    e.stopPropagation();
    document.getElementById('dropZone').classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    e.stopPropagation();
    document.getElementById('dropZone').classList.remove('dragover');
}

function handleFiles(files) {
    const fileInput = document.getElementById('fileInput');
    fileInput.files = files;
    updateFileList(files);
}

document.getElementById('fileInput').addEventListener('change', function(e) {
    updateFileList(this.files);
});

function updateFileList(files) {
    const fileList = document.getElementById('fileList');
    fileList.innerHTML = '';
    
    for (let file of files) {
        const div = document.createElement('div');
        div.className = 'file-preview';
        
        if (file.type.startsWith('image/')) {
            const img = document.createElement('img');
            img.src = URL.createObjectURL(file);
            div.appendChild(img);
        } else {
            const icon = document.createElement('i');
            icon.className = 'fas fa-file fa-2x mr-3';
            div.appendChild(icon);
        }
                        
        div.appendChild(document.createTextNode(file.name));
        fileList.appendChild(div);
    }
}

// Add this function before the file upload form handler
function addFileToList(file) {
    const fileListContainer = document.querySelector(`.list-group`);
    if (!fileListContainer) return;

    const fileItem = document.createElement('div');
    fileItem.id = `file-${file.id}`;
    fileItem.className = 'file-item d-flex justify-content-between align-items-center mb-2 p-2 border rounded';
    
    // Determine icon based on file category
    const iconClass = file.file_category === 'document' ? 'fa-file-alt' : 
                     file.file_category === 'image' ? 'fa-file-image' : 
                     'fa-file';
    
    fileItem.innerHTML = `
        <div class="file-info">
            <i class="fas ${iconClass} mr-2"></i>
            <span class="file-name">${file.file_name}</span>
        </div>
        <button onclick="deleteFile('${file.id}', '${file.assignment_id}')" 
                type="button" class="btn btn-sm btn-outline-danger">
            <i class="fas fa-trash"></i>
        </button>
    `;
    
    // Add to appropriate category section
    const categorySection = file.file_category === 'document' ? 
        document.querySelector('.col-md-6:first-child .list-group') : 
        document.querySelector('.col-md-6:last-child .list-group');
    
    if (categorySection) {
        categorySection.appendChild(fileItem);
    }
}

// Update the file upload form handler
document.getElementById('fileUploadForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    const progressBar = document.querySelector('.progress');
    const progressBarFill = progressBar.querySelector('.progress-bar');
    
    progressBar.style.display = 'block';
    
    fetch(this.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            showAlert('success', 'Files uploaded successfully');
            
            // Add each uploaded file to the appropriate section
            data.files.forEach(file => {
                const listContainer = file.file_category === 'document' ? 
                    document.querySelector('.col-md-6:first-child .list-group') :
                    document.querySelector('.col-md-6:last-child .row');
                
                if (listContainer) {
                    const fileItem = document.createElement('div');
                    fileItem.id = `file-${file.id}`;
                    fileItem.className = 'file-item d-flex justify-content-between align-items-center mb-2 p-2 border rounded';
                    
                    fileItem.innerHTML = `
                        <div class="file-info">
                            <i class="fas ${file.file_category === 'document' ? 'fa-file-alt' : 'fa-file-image'} mr-2"></i>
                            <span class="file-name">${file.name}</span>
                        </div>
                        <button onclick="deleteFile('${file.id}', '${data.assignment_id}')" 
                                type="button" class="btn btn-sm btn-outline-danger">
                            <i class="fas fa-trash"></i>
                        </button>
                    `;
                    
                    listContainer.appendChild(fileItem);
                }
            });
            
            // Clear the file input and preview
            document.getElementById('fileInput').value = '';
            document.getElementById('fileList').innerHTML = '';
            
            if (data.embedding_status === 'pending') {
                showAlert('info', 'Note: File search capabilities will be available once processing is complete');
            }
            
            // Reload the page to show new files
            location.reload();
        } else {
            showAlert('error', data.message || 'Upload failed');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('warning', 'Files uploaded successfully, but search capabilities may be temporarily limited');
    })
    .finally(() => {
        progressBar.style.display = 'none';
    });
});

function deleteFile(fileId, assignmentId) {
    if (confirm('Are you sure you want to delete this file?')) {
        fetch(`/assignments/${assignmentId}/delete-file/${fileId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Remove the file element from the DOM
                const fileElement = document.getElementById(`file-${fileId}`);
                if (fileElement) {
                    fileElement.remove();
                }
                // Show success message
                showAlert('success', 'File deleted successfully');
            } else {
                showAlert('error', data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showAlert('error', 'An error occurred while deleting the file');
        });
    }
}

function showAlert(type, message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            <span aria-hidden="true">&times;</span>
        </button>
    `;
    
    // Insert the alert at the top of the file list
    const fileList = document.querySelector('.file-list');
    if (fileList) {
        fileList.insertBefore(alertDiv, fileList.firstChild);
    }
    
    // Auto-dismiss after 3 seconds
    setTimeout(() => {
        alertDiv.remove();
    }, 3000);
}

async function performSemanticSearch() {
    const query = document.getElementById('semanticSearchInput').value;
    const resultsDiv = document.getElementById('searchResults');
    const assignmentId = getAssignmentIdFromUrl();
    
    if (!query) {
        resultsDiv.innerHTML = '<div class="alert alert-warning">Please enter a search query</div>';
        return;
    }
    
    try {
        resultsDiv.innerHTML = '<div class="text-center"><i class="fas fa-spinner fa-spin"></i> Searching...</div>';
        
        const response = await fetch(`/api/semantic-search/${assignmentId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({ query })
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            resultsDiv.innerHTML = data.results.map(result => `
                <div class="card mb-2 animate__animated animate__fadeIn">
                    <div class="card-body">
                        <h5 class="card-title">${result.file_name}</h5>
                        <p class="card-text">${result.chunk}</p>
                        <small class="text-muted">Relevance: ${(result.similarity * 100).toFixed(1)}%</small>
                    </div>
                </div>
            `).join('') || '<div class="alert alert-info">No results found</div>';
        } else {
            throw new Error(data.message);
        }
    } catch (error) {
        resultsDiv.innerHTML = `<div class="alert alert-danger">Error: ${error.message}</div>`;
    }
}