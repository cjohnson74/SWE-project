// Initialize simulation as a global variable
let simulation;

document.addEventListener("DOMContentLoaded", function() {
    // Pass the courses data from Django view
    console.log("HERE");
    const courses = coursesData;
    console.log(courses);
    
    // Update next assignments panel
    updateNextAssignments(courses);

    // Your existing code for course visualization...
    courses.forEach(course => {
        console.log("\nCourse:", {
            name: course.name,
            course_code: course.course_code,
            assignments: course.assignments
        });
        
        if (course.assignments) {
            course.assignments.forEach(assignment => {
                console.log("\nAssignment:", {
                    name: assignment.name,
                    due_at: assignment.due_at,
                    breakdowns: assignment.breakdowns
                });
                
                if (assignment.breakdowns && assignment.breakdowns[0] && assignment.breakdowns[0].tasks) {
                    console.log("\nTasks:", assignment.breakdowns[0].tasks.map(task => ({
                        task_number: task.task_number,
                        description: task.description,
                        due_date: task.due_date,
                        estimated_time: task.estimated_time
                    })));
                }
            });
        }
    });

    let svg = d3.select("#graph");
    let width = svg.node().getBoundingClientRect().width;
    console.log(width);
    let height = svg.node().getBoundingClientRect().height;
    console.log(height);

    // Calculate the center positions for the bubbles
    const bubbleRadius = 40;
    const centerX = width / 2;
    const centerY = height / 2;

    // Define scales for x and y positions
    const xScale = d3.scaleLinear()
        .domain([0, width])
        .range([0, width]);
    const yScale = d3.scaleLinear()
        .domain([0, height])
        .range([height, 0]);

    // Define the drag behavior
    const drag = d3.drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended);

    function dragstarted(event, d) {
        d3.select(this).raise().classed("active", true);
    }

    function dragged(event, d) {
        // Update the position of the dragged course
        d.x = event.x;
        d.y = event.y;

        // Update the dragged node position
        d3.select(this)
            .attr("cx", d.x)
            .attr("cy", d.y);

        // Update label position if this is a course
        if (d.label) {
            // Calculate the new position for the label
            const labelOffsetX = 259;
            const labelOffsetY = 152;
            d.label.style.left = `${d.x + labelOffsetX}px`;
            d.label.style.top = `${d.y + labelOffsetY}px`;
        }

        if (d3.select(this).classed("bubble")) {
            // If this is a course being dragged
            if (d.visibleAssignments) {
                d.visibleAssignments.forEach(assignment => {
                    // Calculate the new position for each assignment
                    const dx = assignment.x - assignment.sourceCourse.x;
                    const dy = assignment.y - assignment.sourceCourse.y;

                    // Update assignment position
                    assignment.x = d.x + dx;
                    assignment.y = d.y + dy;

                    // Update the visual position of the assignment
                    d3.select(`circle.assignment[data-id="${assignment.id}"]`)
                        .attr("cx", assignment.x)
                        .attr("cy", assignment.y);

                    // Update the link
                    d3.select(assignment.link)
                        .attr("x1", d.x) // Update the start of the link to the new position of the assignment
                        .attr("y1", d.y) // Update the start of the link to the new position of the assignment
                        .attr("x2", assignment.x) // Keep the end of the link at the assignment's position
                        .attr("y2", assignment.y);
                });

                // Update the course's stored position
                d.x = event.x;
                d.y = event.y;
            }
        } else if (d3.select(this).classed("assignment")) {
            // If dragging an assignment, update its link
            d3.select(d.link)
                .attr("x1", d.sourceCourse.x)
                .attr("y1", d.sourceCourse.y)
                .attr("x2", d.x)
                .attr("y2", d.y);
            console.log("Updated link for assignment", d);

            if (d.visibleTasks) {
                d3.select(d.visibleTasks[0].link)
                    .attr("x1", d.x)
                    .attr("y1", d.y);
            }
            
        } else if (d3.select(this).classed("task")) {
            // Update the link coming TO this task
            d3.select(d.link)
                .attr("x2", d.x)
                .attr("y2", d.y);

            // Find and update any link going FROM this task
            const nextTask = d3.selectAll(".task")
                .filter(task => task.source === d);
            
            if (!nextTask.empty()) {
                d3.select(nextTask.datum().link)
                    .attr("x1", d.x)
                    .attr("y1", d.y);
            }
        }
    }

    function dragended(event, d) {
        // If the simulation is running, stop it
        if (!event.active) simulation.alphaTarget(0);

        // Reposition assignments around the course
        if (d.visibleAssignments) {
            const radius = 80; // Adjust the radius as needed
            d.visibleAssignments.forEach((assignment, i) => {
                const angle = (i / d.visibleAssignments.length) * 2 * Math.PI; // Evenly distribute assignments
                assignment.x = d.x + radius * Math.cos(angle);
                assignment.y = d.y + radius * Math.sin(angle);
            });
        }

        // Restart the simulation to apply the new positions
        simulation.nodes(courses.concat(d.visibleAssignments)); // Ensure all nodes are included
        simulation.alpha(0.3).restart();
    }

    // Add this right after your SVG creation to create a group for links that will always be behind nodes
    const linkGroup = svg.append("g").attr("class", "links");
    const nodeGroup = svg.append("g").attr("class", "nodes");

    // Create course nodes for each course
    const courseNodes = nodeGroup.selectAll(".bubble")
        .data(courses)
        .enter()
        .append("g")  // Create a group for each course
        .attr("class", "course-group");

    // Add the circle
    courseNodes.append("circle")
        .attr("class", "bubble")
        .attr("r", bubbleRadius)
        .attr("cx", d => width/2 + (Math.random() - 0.5) * 100)  // Random initial position
        .attr("cy", d => height/2 + (Math.random() - 0.5) * 100) // Random initial position
        .attr("data-toggle", "tooltip")
        .attr("title", d => `
            <div class="custom-tooltip">
                <div class="tooltip-title">${d.name}</div>
                <div class="tooltip-info">
                    <span class="tooltip-icon">📚</span> ${d.course_code}
                </div>
            </div>
        `) // Tooltip content
        .on("click", function(event, d) {
            // Clear both assignments and tasks
            d3.selectAll(".assignment").remove();
            d3.selectAll(".task").remove();
            d3.selectAll(".link").remove();  // This will remove both assignment and task links
            
            // Show assignments for the clicked course
            showAssignments(d.assignments, d3.pointer(event), d);
        })
        .on("mouseover", function() {
            $(this).tooltip('show'); // Show tooltip on hover
        })
        .on("mouseout", function() {
            $(this).tooltip('hide'); // Hide tooltip on mouse out
        })
        .call(drag); // Attach the drag behavior to the bubbles

    // Replace the text label creation with this
    courseNodes.each(function(d) {
        // Create HTML label
        const label = document.createElement('div');
        label.className = 'course-label';
        label.textContent = d.course_code;
        document.body.appendChild(label);

        // Store reference to the label
        d.label = label;

        // Set initial position
        label.style.left = `${d.x}px`;
        label.style.top = `${d.y}px`;
    });

    // Initialize tooltips with the correct options
    $('[data-toggle="tooltip"]').tooltip({
        html: true,
        trigger: 'hover',
        container: 'body',
        template: '<div class="tooltip" role="tooltip"><div class="arrow"></div><div class="tooltip-inner"></div></div>'
    });

    // Modify the simulation
    simulation = d3.forceSimulation(courses)  // Initialize with courses data
        .force("charge", d3.forceManyBody().strength(-100))  // Increased repulsion
        .force("center", d3.forceCenter(width / 2, height / 2).strength(0.05))
        .force("collision", d3.forceCollide().radius(50))  // Prevent overlap
        .force("x", d3.forceX(width / 2).strength(0.1))   // Gentle force toward center x
        .force("y", d3.forceY(height / 2).strength(0.1))  // Gentle force toward center y
        .velocityDecay(0.7) // Add damping to slow down movement (0-1, higher = slower)
        .alphaDecay(0.02) // Slower cooling (smaller number = slower settling)
        .on("tick", ticked);

    

    // Update assignment creation to handle the data structure
    function showAssignments(assignments, position, sourceCourse) {
        console.log("Showing assignments for course:", sourceCourse);
        
        // Only remove assignments and links, not course labels
        d3.selectAll(".assignment").remove();
        d3.selectAll(".link").remove();
        
        // Store assignments with the course
        sourceCourse.visibleAssignments = assignments;
        console.log("Stored assignments:", sourceCourse.visibleAssignments);

        // Position assignments in a circle around the course
        assignments.forEach((assignment, i) => {
            const angle = (i / assignments.length) * 2 * Math.PI;
            const radius = 80;
            assignment.x = sourceCourse.x + radius * Math.cos(angle);
            assignment.y = sourceCourse.y + radius * Math.sin(angle);
            assignment.sourceCourse = sourceCourse;  // Store reference to parent course
            console.log(`Assignment ${i} position:`, {x: assignment.x, y: assignment.y});
        });

        // Create links first
        const links = linkGroup.selectAll(".link")
            .data(assignments)
            .enter()
            .append("line")
            .attr("class", "link");

        // Create assignment nodes
        const assignmentNodes = nodeGroup.selectAll(".assignment")
            .data(assignments)
            .enter()
            .append("circle")
            .attr("class", d => {
                const now = new Date();
                const dueDate = new Date(d.due_at);
                if (dueDate < now) return "assignment overdue";
                return "assignment incomplete";
            })
            .attr("data-id", d => d.id)
            .attr("r", 20)
            .attr("cx", d => position[0] + 100)
            .attr("cy", d => position[1])
            .attr("data-toggle", "tooltip")
            .attr("title", d => {
                const tooltipContent = `
                    <div class="custom-tooltip">
                        <div class="tooltip-title">${d.name}</div>
                        <div class="tooltip-info">
                            <span class="tooltip-icon">📅</span> Due: ${new Date(d.due_at).toLocaleDateString()}
                        </div>
                        <div class="tooltip-info">
                            <span class="tooltip-icon">⭐</span> Points: ${d.points_possible || 'N/A'}
                        </div>
                        <div class="tooltip-info">
                            <span class="tooltip-icon">📝</span> ${d.description || 'No description available'}
                        </div>
                        <div class="tooltip-info">
                            <span class="tooltip-icon">${new Date(d.due_at) < new Date() ? '⚠️' : '✅'}</span> 
                            Status: ${new Date(d.due_at) < new Date() ? 'Overdue' : 'Upcoming'}
                        </div>
                    </div>`;
                console.log('Assignment Tooltip Content:', tooltipContent);
                return tooltipContent;
            })
            .on("click", function(event, d) {
                // Clear existing tasks
                d3.selectAll(".task").remove();
                
                // Clear ALL task-related links
                d3.selectAll(".link")
                    .filter(l => {
                        return l.source && (
                            l.source.constructor.name === 'Task' || 
                            l.source.task_number !== undefined ||
                            (l.target && l.target.task_number !== undefined) ||
                            l.source.breakdowns
                        );
                    })
                    .remove();
                
                // Show tasks for the clicked assignment
                if (d.breakdowns && d.breakdowns[0] && d.breakdowns[0].tasks) {
                    showTasks(d.breakdowns[0].tasks, d3.pointer(event), d);
                }
            })
            .on("mouseover", function() {
                $(this).tooltip('show');
            })
            .on("mouseout", function() {
                $(this).tooltip('hide');
            })
            .call(drag);

        // Store references
        assignmentNodes.each(function(d, i) {
            d.link = links.nodes()[i];
            d.sourceCourse = sourceCourse;
        });

        // Update link positions
        links
            .attr("x1", sourceCourse.x)
            .attr("y1", sourceCourse.y)
            .attr("x2", d => position[0] + 100)
            .attr("y2", position[1]);

        // Update simulation with assignments and tasks
        simulation
            .nodes([...courses, ...assignments]) // Include assignments in the simulation
            .force("link", d3.forceLink().links(links)
                .distance(80)  // Shorter target distance
                .strength(0.2)) // Weaker link force
            .alpha(0.3) // Lower alpha for gentler start
            .restart();

        // Initialize tooltips
        $('[data-toggle="tooltip"]').tooltip({
            html: true,
            trigger: 'hover'
        });
    }

    // Update task creation to handle the data structure
    function showTasks(tasks, position, sourceAssignment) {
        console.log("Showing tasks for assignment:", sourceAssignment);
        d3.selectAll(".task").remove();
        d3.selectAll(".task-link").remove();
        
        // Store tasks with the assignment
        sourceAssignment.visibleTasks = tasks;
        
        // Sort tasks by task_number
        tasks.sort((a, b) => a.task_number - b.task_number);

        // Position tasks in a line extending from the assignment
        const taskSpacing = 40; // Spacing between tasks
        tasks.forEach((task, i) => {
            task.x = sourceAssignment.x + (i + 1) * taskSpacing;
            task.y = sourceAssignment.y;
            // Set the source based on position in chain
            task.source = i === 0 ? sourceAssignment : tasks[i - 1];
        });

        // Create links first (so they appear behind tasks)
        const links = linkGroup.selectAll(".task-link")
            .data(tasks)
            .enter()
            .append("line")
            .attr("class", "link")
            .attr("x1", d => d.source.x)  // Start from previous task or assignment
            .attr("y1", d => d.source.y)
            .attr("x2", d => d.x)
            .attr("y2", d => d.y);

        // Create task nodes
        const taskNodes = nodeGroup.selectAll(".task")
            .data(tasks)
            .enter()
            .append("circle")
            .attr("class", "task")
            .attr("class", d => {
                const now = new Date();
                const dueDate = new Date(d.due_date);
                if (dueDate < now) return "task overdue";
                return "task incomplete";
            })
            .attr("data-id", d => d.task_number)
            .attr("r", 10)
            .attr("cx", d => d.x)
            .attr("cy", d => d.y)
            .attr("data-toggle", "tooltip")
            .attr("title", d => `
                <div class="custom-tooltip">
                    <div class="tooltip-title">Task ${d.task_number}</div>
                    <div class="tooltip-info">
                        <span class="tooltip-icon">📝</span> ${d.description}
                    </div>
                    <div class="tooltip-info">
                        <span class="tooltip-icon">⏱️</span> ${d.estimated_time}
                    </div>
                    <div class="tooltip-info">
                        <span class="tooltip-icon">📅</span> Due: ${new Date(d.due_date).toLocaleDateString()}
                    </div>
                </div>
            `)
            .on("mouseover", function() {
                $(this).tooltip('show');
            })
            .on("mouseout", function() {
                $(this).tooltip('hide');
            })
            .call(drag);

        // Store references
        taskNodes.each(function(d, i) {
            d.link = links.nodes()[i];
        });

        // Initialize tooltips
        $('[data-toggle="tooltip"]').tooltip({
            html: true,
            trigger: 'hover'
        });
    }

    // Function to update positions of nodes
    function ticked() {
        // Update links
        svg.selectAll(".link")
            .attr("x1", d => {
                const source = d.sourceCourse || d.source;
                return source.x;
            })
            .attr("y1", d => {
                const source = d.sourceCourse || d.source;
                return source.y;
            })
            .attr("x2", d => d.x)
            .attr("y2", d => d.y);

        // Update course groups
        const courseGroups = svg.selectAll(".course-group");
        courseGroups.selectAll("circle")
            .attr("cx", d => d.x)
            .attr("cy", d => d.y);
        
        // Update assignment positions
        svg.selectAll(".assignment")
            .attr("cx", d => d.x)
            .attr("cy", d => d.y);

        // Update HTML labels
        courses.forEach(d => {
            if (d.label) {
                const svgRect = svg.node().getBoundingClientRect();
                const labelX = svgRect.left + d.x; // X position relative to the SVG
                const labelY = svgRect.top + d.y;  // Y position relative to the SVG

                // Adjust label position based on scroll
                d.label.style.left = `${labelX + window.scrollX}px`;
                d.label.style.top = `${labelY + window.scrollY}px`; // Add window scroll position
            }
        });
    }

    $('[data-toggle="tooltip"]').tooltip({
        html: true,
        trigger: 'hover',
        container: 'body',
        template: '<div class="tooltip" role="tooltip"><div class="arrow"></div><div class="tooltip-inner"></div></div>'
    });
});

// Add the new updateNextAssignments function
function updateNextAssignments(courses) {
    const now = new Date();
    let allAssignments = [];
    
    // Collect all assignments with their course info
    courses.forEach(course => {
        if (course.assignments) {
            course.assignments.forEach(assignment => {
                if (assignment.due_at) {
                    allAssignments.push({
                        ...assignment,
                        courseName: course.name,
                        courseCode: course.course_code
                    });
                }
            });
        }
    });
    
    // Sort assignments by due date
    allAssignments.sort((a, b) => new Date(a.due_at) - new Date(b.due_at));
    
    // Filter to only show upcoming assignments (not past due)
    const upcomingAssignments = allAssignments.filter(a => new Date(a.due_at) > now);
    
    // Take the next 3 assignments
    const nextAssignments = upcomingAssignments.slice(0, 3);
    
    // Update the display
    const container = document.getElementById('nextAssignments');
    container.innerHTML = nextAssignments.length ? '' : '<p>No upcoming assignments!</p>';
    
    nextAssignments.forEach((assignment, index) => {
        const dueDate = new Date(assignment.due_at);
        const timeRemaining = Math.ceil((dueDate - now) / (1000 * 60 * 60 * 24));
        
        const div = document.createElement('div');
        div.className = `priority-assignment ${timeRemaining <= 3 ? 'priority-urgent' : 'priority-upcoming'}`;
        
        div.innerHTML = `
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <span class="course-tag">${assignment.courseCode}</span>
                    <strong>${assignment.name}</strong>
                </div>
                <div class="time-remaining">
                    ${timeRemaining} day${timeRemaining !== 1 ? 's' : ''} remaining
                </div>
            </div>
            <div class="progress mt-2" style="height: 4px;">
                <div class="progress-bar ${timeRemaining <= 3 ? 'bg-danger' : 'bg-warning'}" 
                     role="progressbar" 
                     style="width: ${100 - (timeRemaining / 14) * 100}%">
                </div>
            </div>
        `;
        
        container.appendChild(div);
    });
}

// Call on load and window resize
window.addEventListener('load', updateSvgDimensions);
window.addEventListener('resize', updateSvgDimensions);