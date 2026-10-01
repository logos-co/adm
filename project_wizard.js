// Project Portfolio Wizard JavaScript
// Interactive project creation and stakeholder evaluation system

// Global variables
let projects = [];
let evaluations = [];
let currentEvaluationType = null;
let constraintData = null;

/**
 * Escape a value for safe interpolation into an HTML template literal.
 *
 * Every value rendered below reaches the DOM through `innerHTML`, and the values
 * are user supplied: they arrive from form fields, from `localStorage`, and from
 * exported/imported JSON files that can be shared between users. Interpolating
 * them raw means a value such as `<img src=x onerror=...>` is parsed as markup,
 * which is a stored cross-site-scripting vector. Escaping the five characters
 * that matter for element content and quoted attribute contexts removes it.
 *
 * Use this on any interpolated value that is not a literal defined in this file.
 * `textContent` is preferable where a whole text node is being set, because it
 * needs no escaping at all.
 */
function escapeHtml(value) {
    if (value === null || value === undefined) {
        return '';
    }
    return String(value)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeSliders();
    initializeValidation();
    loadExistingData();
    setupEventListeners();
});

// Tab management
function showTab(tabName) {
    // Hide all tab contents
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(tab => tab.classList.remove('active'));
    
    // Remove active class from all nav tabs
    const navTabs = document.querySelectorAll('.nav-tab');
    navTabs.forEach(tab => tab.classList.remove('active'));
    
    // Show selected tab content
    document.getElementById(tabName).classList.add('active');
    
    // Add active class to clicked nav tab
    event.target.classList.add('active');
    
    // Update progress and load data based on tab
    switch(tabName) {
        case 'project-creation':
            updateProgress(25);
            break;
        case 'stakeholder-evaluation':
            updateProgress(50);
            loadProjectsForEvaluation();
            break;
        case 'constraint-analysis':
            updateProgress(75);
            generateConstraintAnalysis();
            break;
        case 'export-results':
            updateProgress(100);
            prepareExportData();
            break;
    }
}

// Progress bar management
function updateProgress(percentage) {
    const progressFill = document.querySelector('.progress-fill');
    if (progressFill) {
        progressFill.style.width = percentage + '%';
    }
}

// Initialize slider displays
function initializeSliders() {
    const sliders = document.querySelectorAll('.score-slider');
    sliders.forEach(slider => {
        const displayId = slider.id + '-display';
        const display = document.getElementById(displayId);
        
        if (display) {
            // Update display on input
            slider.addEventListener('input', function() {
                display.textContent = parseFloat(this.value).toFixed(2);
            });
            
            // Set initial value
            display.textContent = parseFloat(slider.value).toFixed(2);
        }
    });
}

// Form validation
function initializeValidation() {
    // Character counter for description
    const descTextarea = document.getElementById('project-description');
    const descCounter = document.getElementById('desc-count');
    
    if (descTextarea && descCounter) {
        descTextarea.addEventListener('input', function() {
            descCounter.textContent = this.value.length;
            
            if (this.value.length > 500) {
                descCounter.style.color = '#dc3545';
            } else {
                descCounter.style.color = '#6c757d';
            }
        });
    }
    
    // Date validation
    const startDate = document.getElementById('start-date');
    const endDate = document.getElementById('end-date');
    
    if (startDate && endDate) {
        function validateDates() {
            if (startDate.value && endDate.value) {
                if (new Date(startDate.value) >= new Date(endDate.value)) {
                    showValidationError('end-date', 'End date must be after start date');
                    return false;
                } else {
                    hideValidationError('end-date');
                    return true;
                }
            }
            return true;
        }
        
        startDate.addEventListener('change', validateDates);
        endDate.addEventListener('change', validateDates);
    }
}

// Validation helper functions
function showValidationError(fieldId, message) {
    const errorElement = document.getElementById(fieldId + '-error');
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.style.display = 'block';
    }
    
    const field = document.getElementById(fieldId);
    if (field) {
        field.style.borderColor = '#dc3545';
    }
}

function hideValidationError(fieldId) {
    const errorElement = document.getElementById(fieldId + '-error');
    if (errorElement) {
        errorElement.style.display = 'none';
    }
    
    const field = document.getElementById(fieldId);
    if (field) {
        field.style.borderColor = '#e9ecef';
    }
}

// Project form validation and saving
function validateAndSaveProject() {
    const form = document.getElementById('project-form');
    const formData = new FormData(form);
    const project = {};
    
    // Convert form data to object
    for (let [key, value] of formData.entries()) {
        project[key] = value;
    }
    
    // Validate required fields
    const requiredFields = ['project_id', 'name', 'description', 'status', 'start_date', 'end_date', 'strategic_priority', 'risk_level'];
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!project[field] || project[field].trim() === '') {
            showValidationError(field.replace('_', '-'), 'This field is required');
            isValid = false;
        } else {
            hideValidationError(field.replace('_', '-'));
        }
    });
    
    // Validate project ID uniqueness
    if (projects.some(p => p.project_id === project.project_id)) {
        showValidationError('project-id', 'Project ID must be unique');
        isValid = false;
    }
    
    // Validate date logic
    if (project.start_date && project.end_date) {
        if (new Date(project.start_date) >= new Date(project.end_date)) {
            showValidationError('end-date', 'End date must be after start date');
            isValid = false;
        }
    }
    
    // Validate JSON fields
    const jsonFields = ['risk_factors', 'cooperation_projects', 'precedence_projects', 'exclusive_projects', 'technology_stack', 'success_metrics'];
    jsonFields.forEach(field => {
        if (project[field] && project[field].trim() !== '') {
            try {
                project[field] = JSON.parse(project[field]);
            } catch (e) {
                showValidationError(field.replace('_', '-'), 'Invalid JSON format');
                isValid = false;
            }
        } else {
            project[field] = [];
        }
    });
    
    // Convert numeric fields
    const numericFields = ['construction_duration', 'team_size', 'budget_allocated', 'construction_cost', 'completion_percentage'];
    numericFields.forEach(field => {
        if (project[field]) {
            project[field] = parseFloat(project[field]);
        }
    });
    
    // Convert slider values
    const sliderFields = ['strategic_value', 'technical_complexity', 'market_impact', 'resource_requirement', 'innovation_level'];
    sliderFields.forEach(field => {
        if (project[field]) {
            project[field] = parseFloat(project[field]);
        }
    });
    
    if (isValid) {
        // Add metadata
        project.created_date = new Date().toISOString().split('T')[0];
        project.last_updated = new Date().toISOString().split('T')[0];
        
        // Save project
        projects.push(project);
        saveToLocalStorage();
        
        // Show success message
        showSuccessMessage('Project saved successfully!');
        
        // Clear form
        setTimeout(() => {
            clearForm();
        }, 2000);
    }
}

// Clear form
function clearForm() {
    const form = document.getElementById('project-form');
    form.reset();
    
    // Reset sliders
    const sliders = document.querySelectorAll('.score-slider');
    sliders.forEach(slider => {
        slider.value = 0.5;
        const displayId = slider.id + '-display';
        const display = document.getElementById(displayId);
        if (display) {
            display.textContent = '0.50';
        }
    });
    
    // Hide all validation errors
    const errors = document.querySelectorAll('.validation-error');
    errors.forEach(error => error.style.display = 'none');
    
    // Reset field borders
    const fields = document.querySelectorAll('input, textarea, select');
    fields.forEach(field => field.style.borderColor = '#e9ecef');
}

// Success message
function showSuccessMessage(message) {
    // Create success notification
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #28a745, #1e7e34);
        color: white;
        padding: 15px 25px;
        border-radius: 8px;
        box-shadow: 0 5px 15px rgba(40,167,69,0.3);
        z-index: 1000;
        font-weight: 600;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        document.body.removeChild(notification);
    }, 3000);
}

// Stakeholder evaluation functions
function selectEvaluationType(type) {
    currentEvaluationType = type;
    
    // Update UI
    const cards = document.querySelectorAll('.evaluation-type-card');
    cards.forEach(card => card.classList.remove('selected'));
    
    event.target.closest('.evaluation-type-card').classList.add('selected');
    
    // Show appropriate form
    showEvaluationForm(type);
}

function showEvaluationForm(type) {
    const container = document.getElementById('structured-evaluation-form');
    if (!container) return;
    
    let formHTML = '';
    
    switch(type) {
        case 'comparison':
            formHTML = `
                <div class="evaluation-card">
                    <h4>⚖️ Project Comparison</h4>
                    <div class="form-row">
                        <div class="form-group">
                            <label>First Project</label>
                            <select id="comparison-project-a">
                                <option value="">Select project...</option>
                                ${getProjectOptions()}
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Second Project</label>
                            <select id="comparison-project-b">
                                <option value="">Select project...</option>
                                ${getProjectOptions()}
                            </select>
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label>Comparison Operator</label>
                            <select id="comparison-operator">
                                <option value="GREATER">Greater than (>)</option>
                                <option value="LESS">Less than (<)</option>
                                <option value="EQUAL">Equal to (=)</option>
                                <option value="GREATER_EQUAL">Greater than or equal (>=)</option>
                                <option value="LESS_EQUAL">Less than or equal (<=)</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Criteria</label>
                            <select id="comparison-criteria">
                                <option value="Strategic Value">Strategic Value</option>
                                <option value="Technical Complexity">Technical Complexity</option>
                                <option value="Market Impact">Market Impact</option>
                                <option value="Resource Requirement">Resource Requirement</option>
                                <option value="Innovation Level">Innovation Level</option>
                            </select>
                        </div>
                    </div>
                    <div class="form-group">
                        <label>Confidence (0.0-1.0)</label>
                        <input type="range" id="comparison-confidence" min="0" max="1" step="0.1" value="1.0">
                        <div class="score-display" id="comparison-confidence-display">1.00</div>
                    </div>
                    <button type="button" class="btn btn-primary" onclick="addComparison()">Add Comparison</button>
                </div>
            `;
            break;
            
        case 'range':
            formHTML = `
                <div class="evaluation-card">
                    <h4>📏 Value Range</h4>
                    <div class="form-group">
                        <label>Project</label>
                        <select id="range-project">
                            <option value="">Select project...</option>
                            ${getProjectOptions()}
                        </select>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label>Minimum Value</label>
                            <input type="number" id="range-min" min="0" max="1" step="0.05" placeholder="0.0">
                        </div>
                        <div class="form-group">
                            <label>Maximum Value</label>
                            <input type="number" id="range-max" min="0" max="1" step="0.05" placeholder="1.0">
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label>Criteria</label>
                            <select id="range-criteria">
                                <option value="Strategic Value">Strategic Value</option>
                                <option value="Technical Complexity">Technical Complexity</option>
                                <option value="Market Impact">Market Impact</option>
                                <option value="Resource Requirement">Resource Requirement</option>
                                <option value="Innovation Level">Innovation Level</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Confidence (0.0-1.0)</label>
                            <input type="range" id="range-confidence" min="0" max="1" step="0.1" value="1.0">
                            <div class="score-display" id="range-confidence-display">1.00</div>
                        </div>
                    </div>
                    <button type="button" class="btn btn-primary" onclick="addRange()">Add Range</button>
                </div>
            `;
            break;
            
        case 'ranking':
            formHTML = `
                <div class="evaluation-card">
                    <h4>📊 Project Ranking</h4>
                    <div class="form-group">
                        <label>Projects (in order of preference)</label>
                        <div id="ranking-projects">
                            ${getProjectCheckboxes()}
                        </div>
                        <div class="help-text">Select projects to rank</div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label>Criteria</label>
                            <select id="ranking-criteria">
                                <option value="Strategic Value">Strategic Value</option>
                                <option value="Technical Complexity">Technical Complexity</option>
                                <option value="Market Impact">Market Impact</option>
                                <option value="Resource Requirement">Resource Requirement</option>
                                <option value="Innovation Level">Innovation Level</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Confidence (0.0-1.0)</label>
                            <input type="range" id="ranking-confidence" min="0" max="1" step="0.1" value="1.0">
                            <div class="score-display" id="ranking-confidence-display">1.00</div>
                        </div>
                    </div>
                    <button type="button" class="btn btn-primary" onclick="addRanking()">Add Ranking</button>
                </div>
            `;
            break;
            
        case 'threshold':
            formHTML = `
                <div class="evaluation-card">
                    <h4>🎯 Threshold Constraint</h4>
                    <div class="form-group">
                        <label>Project</label>
                        <select id="threshold-project">
                            <option value="">Select project...</option>
                            ${getProjectOptions()}
                        </select>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label>Threshold Value</label>
                            <input type="number" id="threshold-value" min="0" max="1" step="0.05" placeholder="0.5">
                        </div>
                        <div class="form-group">
                            <label>Operator</label>
                            <select id="threshold-operator">
                                <option value="GREATER_EQUAL">Greater than or equal (>=)</option>
                                <option value="LESS_EQUAL">Less than or equal (<=)</option>
                                <option value="GREATER">Greater than (>)</option>
                                <option value="LESS">Less than (<)</option>
                            </select>
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label>Criteria</label>
                            <select id="threshold-criteria">
                                <option value="Strategic Value">Strategic Value</option>
                                <option value="Technical Complexity">Technical Complexity</option>
                                <option value="Market Impact">Market Impact</option>
                                <option value="Resource Requirement">Resource Requirement</option>
                                <option value="Innovation Level">Innovation Level</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Confidence (0.0-1.0)</label>
                            <input type="range" id="threshold-confidence" min="0" max="1" step="0.1" value="1.0">
                            <div class="score-display" id="threshold-confidence-display">1.00</div>
                        </div>
                    </div>
                    <button type="button" class="btn btn-primary" onclick="addThreshold()">Add Threshold</button>
                </div>
            `;
            break;
    }
    
    container.innerHTML = formHTML;
    
    // Initialize confidence sliders
    const confidenceSliders = container.querySelectorAll('input[type="range"]');
    confidenceSliders.forEach(slider => {
        const displayId = slider.id + '-display';
        const display = document.getElementById(displayId);
        
        if (display) {
            slider.addEventListener('input', function() {
                display.textContent = parseFloat(this.value).toFixed(2);
            });
        }
    });
}

// Helper functions for evaluation forms
function getProjectOptions() {
    return projects.map(p => `<option value="${escapeHtml(p.project_id)}">${escapeHtml(p.name)}</option>`).join('');
}

function getProjectCheckboxes() {
    return projects.map(p => `
        <div style="margin: 5px 0;">
            <input type="checkbox" id="rank-${escapeHtml(p.project_id)}" value="${escapeHtml(p.project_id)}">
            <label for="rank-${escapeHtml(p.project_id)}">${escapeHtml(p.name)}</label>
        </div>
    `).join('');
}

// Add evaluation functions
function addComparison() {
    const evaluatorId = document.getElementById('evaluator-id').value;
    const projectA = document.getElementById('comparison-project-a').value;
    const projectB = document.getElementById('comparison-project-b').value;
    const operator = document.getElementById('comparison-operator').value;
    const criteria = document.getElementById('comparison-criteria').value;
    const confidence = parseFloat(document.getElementById('comparison-confidence').value);
    
    if (!evaluatorId || !projectA || !projectB) {
        alert('Please fill in all required fields');
        return;
    }
    
    const evaluation = {
        evaluator_id: evaluatorId,
        evaluation_type: 'COMPARISON',
        projects: [projectA, projectB],
        operator: operator,
        criteria: criteria,
        confidence: confidence,
        timestamp: new Date().toISOString()
    };
    
    evaluations.push(evaluation);
    updateEvaluationsList();
    saveToLocalStorage();
    showSuccessMessage('Comparison evaluation added!');
}

function addRange() {
    const evaluatorId = document.getElementById('evaluator-id').value;
    const project = document.getElementById('range-project').value;
    const minVal = parseFloat(document.getElementById('range-min').value);
    const maxVal = parseFloat(document.getElementById('range-max').value);
    const criteria = document.getElementById('range-criteria').value;
    const confidence = parseFloat(document.getElementById('range-confidence').value);
    
    if (!evaluatorId || !project || isNaN(minVal) || isNaN(maxVal)) {
        alert('Please fill in all required fields');
        return;
    }
    
    if (minVal >= maxVal) {
        alert('Minimum value must be less than maximum value');
        return;
    }
    
    const evaluation = {
        evaluator_id: evaluatorId,
        evaluation_type: 'RANGE',
        projects: [project],
        values: [minVal, maxVal],
        criteria: criteria,
        confidence: confidence,
        timestamp: new Date().toISOString()
    };
    
    evaluations.push(evaluation);
    updateEvaluationsList();
    saveToLocalStorage();
    showSuccessMessage('Range evaluation added!');
}

function addRanking() {
    const evaluatorId = document.getElementById('evaluator-id').value;
    const criteria = document.getElementById('ranking-criteria').value;
    const confidence = parseFloat(document.getElementById('ranking-confidence').value);
    
    // Get selected projects in order
    const checkboxes = document.querySelectorAll('#ranking-projects input[type="checkbox"]:checked');
    const selectedProjects = Array.from(checkboxes).map(cb => cb.value);
    
    if (!evaluatorId || selectedProjects.length < 2) {
        alert('Please select at least 2 projects for ranking');
        return;
    }
    
    const evaluation = {
        evaluator_id: evaluatorId,
        evaluation_type: 'RANKING',
        projects: selectedProjects,
        criteria: criteria,
        confidence: confidence,
        timestamp: new Date().toISOString()
    };
    
    evaluations.push(evaluation);
    updateEvaluationsList();
    saveToLocalStorage();
    showSuccessMessage('Ranking evaluation added!');
}

function addThreshold() {
    const evaluatorId = document.getElementById('evaluator-id').value;
    const project = document.getElementById('threshold-project').value;
    const value = parseFloat(document.getElementById('threshold-value').value);
    const operator = document.getElementById('threshold-operator').value;
    const criteria = document.getElementById('threshold-criteria').value;
    const confidence = parseFloat(document.getElementById('threshold-confidence').value);
    
    if (!evaluatorId || !project || isNaN(value)) {
        alert('Please fill in all required fields');
        return;
    }
    
    const evaluation = {
        evaluator_id: evaluatorId,
        evaluation_type: 'THRESHOLD',
        projects: [project],
        operator: operator,
        values: [value],
        criteria: criteria,
        confidence: confidence,
        timestamp: new Date().toISOString()
    };
    
    evaluations.push(evaluation);
    updateEvaluationsList();
    saveToLocalStorage();
    showSuccessMessage('Threshold evaluation added!');
}

// Natural language parsing
function parseNaturalLanguage() {
    const text = document.getElementById('natural-language-input').value;
    const evaluatorId = document.getElementById('evaluator-id').value;
    
    if (!text.trim() || !evaluatorId) {
        alert('Please enter evaluator ID and evaluation text');
        return;
    }
    
    // Simple parsing logic (in a real implementation, this would use the Python NLP parser)
    const parsedEvaluations = parseEvaluationText(text, evaluatorId);
    
    // Display parsed results
    displayParsedEvaluations(parsedEvaluations);
    
    // Add to evaluations list
    evaluations.push(...parsedEvaluations);
    updateEvaluationsList();
    saveToLocalStorage();
}

function parseEvaluationText(text, evaluatorId) {
    const evaluations = [];
    const lines = text.split('\n').filter(line => line.trim());
    
    lines.forEach(line => {
        line = line.trim().toLowerCase();
        
        // Simple comparison parsing
        const comparisonMatch = line.match(/(\w+)\s+(?:is\s+)?(?:better|greater|higher)\s+(?:than\s+)?(\w+)/);
        if (comparisonMatch) {
            evaluations.push({
                evaluator_id: evaluatorId,
                evaluation_type: 'COMPARISON',
                projects: [comparisonMatch[1], comparisonMatch[2]],
                operator: 'GREATER',
                criteria: 'Strategic Value',
                confidence: 1.0,
                timestamp: new Date().toISOString()
            });
        }
        
        // Simple range parsing
        const rangeMatch = line.match(/(\w+)\s+(?:should\s+be\s+)?between\s+([\d.]+)\s+and\s+([\d.]+)/);
        if (rangeMatch) {
            evaluations.push({
                evaluator_id: evaluatorId,
                evaluation_type: 'RANGE',
                projects: [rangeMatch[1]],
                values: [parseFloat(rangeMatch[2]), parseFloat(rangeMatch[3])],
                criteria: 'Strategic Value',
                confidence: 1.0,
                timestamp: new Date().toISOString()
            });
        }
        
        // Simple threshold parsing
        const thresholdMatch = line.match(/(\w+)\s+(?:must\s+be\s+)?(?:at\s+least\s+)([\d.]+)/);
        if (thresholdMatch) {
            evaluations.push({
                evaluator_id: evaluatorId,
                evaluation_type: 'THRESHOLD',
                projects: [thresholdMatch[1]],
                operator: 'GREATER_EQUAL',
                values: [parseFloat(thresholdMatch[2])],
                criteria: 'Strategic Value',
                confidence: 1.0,
                timestamp: new Date().toISOString()
            });
        }
    });
    
    return evaluations;
}

function displayParsedEvaluations(parsedEvaluations) {
    const container = document.getElementById('parsed-results');
    const parsedSection = document.getElementById('parsed-evaluations');
    
    if (parsedEvaluations.length === 0) {
        container.innerHTML = '<p>No evaluations could be parsed from the input text.</p>';
    } else {
        container.innerHTML = parsedEvaluations.map(eval => `
            <div class="parsed-evaluation">
                <strong>${escapeHtml(eval.evaluation_type)}</strong>:
                ${escapeHtml(eval.projects.join(' vs '))}
                ${eval.operator ? `(${escapeHtml(eval.operator)})` : ''}
                ${eval.values ? `[${escapeHtml(eval.values.join(', '))}]` : ''}
                <br><small>Criteria: ${escapeHtml(eval.criteria)}, Confidence: ${escapeHtml(eval.confidence)}</small>
            </div>
        `).join('');
    }
    
    parsedSection.style.display = 'block';
}

// Update evaluations list
function updateEvaluationsList() {
    const container = document.getElementById('current-evaluations-list');
    if (!container) return;
    
    if (evaluations.length === 0) {
        container.innerHTML = '<p>No evaluations added yet.</p>';
    } else {
        container.innerHTML = evaluations.map((eval, index) => `
            <div class="evaluation-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>${escapeHtml(eval.evaluation_type)}</strong> by ${escapeHtml(eval.evaluator_id)}
                        <br><small>${escapeHtml(eval.projects.join(' vs '))} - ${escapeHtml(eval.criteria)}</small>
                    </div>
                    <button class="btn btn-danger" onclick="removeEvaluation(${index})" style="padding: 5px 10px; font-size: 0.9em;">
                        🗑️ Remove
                    </button>
                </div>
            </div>
        `).join('');
    }
}

function removeEvaluation(index) {
    evaluations.splice(index, 1);
    updateEvaluationsList();
    saveToLocalStorage();
}

// Load projects for evaluation
function loadProjectsForEvaluation() {
    const container = document.getElementById('available-projects');
    if (!container) return;
    
    if (projects.length === 0) {
        container.innerHTML = '<p>No projects available. Please create projects first.</p>';
    } else {
        container.innerHTML = `
            <div class="project-list">
                ${projects.map(project => `
                    <div class="project-card">
                        <h4>${escapeHtml(project.name)}</h4>
                        <p><strong>ID:</strong> ${escapeHtml(project.project_id)}</p>
                        <p><strong>Status:</strong> ${escapeHtml(project.status)}</p>
                        <p><strong>Priority:</strong> ${escapeHtml(project.strategic_priority)}</p>
                        <p>${escapeHtml(project.description)}</p>
                    </div>
                `).join('')}
            </div>
        `;
    }
}

// Constraint analysis
function generateConstraintAnalysis() {
    const container = document.getElementById('constraint-analysis-results');
    if (!container) return;
    
    if (evaluations.length === 0) {
        container.innerHTML = '<p>No evaluations available for constraint analysis. Please add evaluations first.</p>';
        return;
    }
    
    // Generate constraint matrices (simplified version)
    const constraints = generateConstraintMatrices();
    displayConstraintAnalysis(constraints);
}

function generateConstraintMatrices() {
    // This is a simplified version - in a real implementation, 
    // this would use the Python QualitativeEvaluationTranslator
    
    const projectIds = [...new Set(projects.map(p => p.project_id))];
    const criteria = ['Strategic Value', 'Technical Complexity', 'Market Impact', 'Resource Requirement', 'Innovation Level'];
    
    const constraints = {
        projects: projectIds,
        criteria: criteria,
        evaluations: evaluations,
        inequalities: [],
        equalities: []
    };
    
    // Convert evaluations to constraints
    evaluations.forEach(eval => {
        switch(eval.evaluation_type) {
            case 'COMPARISON':
                constraints.inequalities.push({
                    type: 'comparison',
                    projects: eval.projects,
                    operator: eval.operator,
                    criteria: eval.criteria,
                    evaluator: eval.evaluator_id
                });
                break;
                
            case 'RANGE':
                constraints.inequalities.push({
                    type: 'range',
                    project: eval.projects[0],
                    min: eval.values[0],
                    max: eval.values[1],
                    criteria: eval.criteria,
                    evaluator: eval.evaluator_id
                });
                break;
                
            case 'THRESHOLD':
                constraints.inequalities.push({
                    type: 'threshold',
                    project: eval.projects[0],
                    operator: eval.operator,
                    value: eval.values[0],
                    criteria: eval.criteria,
                    evaluator: eval.evaluator_id
                });
                break;
        }
    });
    
    return constraints;
}

function displayConstraintAnalysis(constraints) {
    const container = document.getElementById('constraint-analysis-results');
    
    let html = `
        <div class="constraint-visualization">
            <h3>📊 Constraint Analysis Results</h3>
            
            <div class="form-section">
                <h4>📋 Summary</h4>
                <div class="form-row">
                    <div class="form-group">
                        <strong>Projects:</strong> ${constraints.projects.length}
                    </div>
                    <div class="form-group">
                        <strong>Evaluations:</strong> ${constraints.evaluations.length}
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <strong>Inequality Constraints:</strong> ${constraints.inequalities.length}
                    </div>
                    <div class="form-group">
                        <strong>Equality Constraints:</strong> ${constraints.equalities.length}
                    </div>
                </div>
            </div>
            
            <div class="form-section">
                <h4>🔗 Generated Constraints</h4>
                <div id="constraints-list">
                    ${constraints.inequalities.map((constraint, index) => `
                        <div class="evaluation-card">
                            <strong>${escapeHtml(constraint.type.toUpperCase())}</strong> - ${escapeHtml(constraint.criteria)}
                            <br><small>By: ${escapeHtml(constraint.evaluator)}</small>
                            <br><small>Details: ${escapeHtml(JSON.stringify(constraint, null, 2))}</small>
                        </div>
                    `).join('')}
                </div>
            </div>
            
            <div class="form-section">
                <h4>⚠️ Constraint Validation</h4>
                <div id="validation-results">
                    ${validateConstraints(constraints)}
                </div>
            </div>
        </div>
    `;
    
    container.innerHTML = html;
}

function validateConstraints(constraints) {
    const issues = [];
    
    // Check for conflicting constraints
    const comparisons = constraints.inequalities.filter(c => c.type === 'comparison');
    const ranges = constraints.inequalities.filter(c => c.type === 'range');
    const thresholds = constraints.inequalities.filter(c => c.type === 'threshold');
    
    // Check for contradictory comparisons
    for (let i = 0; i < comparisons.length; i++) {
        for (let j = i + 1; j < comparisons.length; j++) {
            const c1 = comparisons[i];
            const c2 = comparisons[j];
            
            if (c1.criteria === c2.criteria && 
                c1.projects[0] === c2.projects[1] && 
                c1.projects[1] === c2.projects[0] &&
                c1.operator === 'GREATER' && c2.operator === 'GREATER') {
                issues.push(`Contradictory comparisons: ${c1.projects[0]} > ${c1.projects[1]} and ${c2.projects[0]} > ${c2.projects[1]}`);
            }
        }
    }
    
    // Check for impossible ranges
    ranges.forEach(range => {
        if (range.min >= range.max) {
            issues.push(`Invalid range for ${range.project}: min (${range.min}) >= max (${range.max})`);
        }
    });
    
    if (issues.length === 0) {
        return '<div style="color: #28a745;">✅ No constraint conflicts detected</div>';
    } else {
        return issues.map(issue => `<div style="color: #dc3545;">❌ ${escapeHtml(issue)}</div>`).join('');
    }
}

// Export functions
function prepareExportData() {
    const container = document.getElementById('export-data-preview');
    if (!container) return;
    
    const exportData = {
        projects: projects,
        evaluations: evaluations,
        constraints: constraintData,
        timestamp: new Date().toISOString(),
        summary: {
            total_projects: projects.length,
            total_evaluations: evaluations.length,
            evaluators: [...new Set(evaluations.map(e => e.evaluator_id))],
            criteria: [...new Set(evaluations.map(e => e.criteria))]
        }
    };
    
    container.innerHTML = `
        <div class="export-section">
            <h3>📊 Export Data Preview</h3>
            <div class="form-row">
                <div class="form-group">
                    <strong>Projects:</strong> ${exportData.summary.total_projects}
                </div>
                <div class="form-group">
                    <strong>Evaluations:</strong> ${exportData.summary.total_evaluations}
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <strong>Evaluators:</strong> ${escapeHtml(exportData.summary.evaluators.join(', '))}
                </div>
                <div class="form-group">
                    <strong>Criteria:</strong> ${escapeHtml(exportData.summary.criteria.join(', '))}
                </div>
            </div>
            
            <div class="export-buttons">
                <button class="btn btn-primary" onclick="exportToJSON()">📄 Export JSON</button>
                <button class="btn btn-primary" onclick="exportToCSV()">📊 Export CSV</button>
                <button class="btn btn-primary" onclick="exportToPython()">🐍 Export Python</button>
            </div>
        </div>
    `;
}

function exportToJSON() {
    const data = {
        projects: projects,
        evaluations: evaluations,
        timestamp: new Date().toISOString()
    };
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    downloadFile(blob, 'portfolio_data.json');
}

function exportToCSV() {
    // Export projects as CSV
    const projectHeaders = ['project_id', 'name', 'description', 'status', 'start_date', 'end_date', 'strategic_priority', 'risk_level'];
    const projectRows = projects.map(p => projectHeaders.map(h => p[h] || '').join(','));
    const projectCSV = [projectHeaders.join(','), ...projectRows].join('\n');
    
    // Export evaluations as CSV
    const evalHeaders = ['evaluator_id', 'evaluation_type', 'projects', 'operator', 'values', 'criteria', 'confidence', 'timestamp'];
    const evalRows = evaluations.map(e => [
        e.evaluator_id,
        e.evaluation_type,
        e.projects.join(';'),
        e.operator || '',
        e.values ? e.values.join(';') : '',
        e.criteria,
        e.confidence,
        e.timestamp
    ].join(','));
    const evalCSV = [evalHeaders.join(','), ...evalRows].join('\n');
    
    const combinedCSV = `PROJECTS\n${projectCSV}\n\nEVALUATIONS\n${evalCSV}`;
    const blob = new Blob([combinedCSV], { type: 'text/csv' });
    downloadFile(blob, 'portfolio_data.csv');
}

function exportToPython() {
    const pythonCode = `
# Generated Portfolio Data for Python Analysis
# Generated on: ${new Date().toISOString()}

import json
from datetime import datetime

# Project data
projects = ${JSON.stringify(projects, null, 4)}

# Evaluation data  
evaluations = ${JSON.stringify(evaluations, null, 4)}

# Usage example:
# from qualitative_evaluation_translator import QualitativeEvaluationTranslator
# translator = QualitativeEvaluationTranslator(
#     projects=[p['project_id'] for p in projects],
#     criteria=['Strategic Value', 'Technical Complexity', 'Market Impact', 'Resource Requirement', 'Innovation Level']
# )
# 
# for eval_data in evaluations:
#     # Convert to QualitativeEvaluation object and add to translator
#     pass

print(f"Loaded {len(projects)} projects and {len(evaluations)} evaluations")
`;
    
    const blob = new Blob([pythonCode], { type: 'text/python' });
    downloadFile(blob, 'portfolio_data.py');
}

function downloadFile(blob, filename) {
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    showSuccessMessage(`Downloaded ${filename}`);
}

// Local storage functions
function saveToLocalStorage() {
    localStorage.setItem('portfolio_projects', JSON.stringify(projects));
    localStorage.setItem('portfolio_evaluations', JSON.stringify(evaluations));
}

function loadExistingData() {
    const savedProjects = localStorage.getItem('portfolio_projects');
    const savedEvaluations = localStorage.getItem('portfolio_evaluations');
    
    if (savedProjects) {
        projects = JSON.parse(savedProjects);
    }
    
    if (savedEvaluations) {
        evaluations = JSON.parse(savedEvaluations);
    }
}

function setupEventListeners() {
    // Add any additional event listeners here
    console.log('Project Portfolio Wizard initialized');
}
