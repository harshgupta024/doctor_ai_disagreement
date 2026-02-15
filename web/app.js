// State Management
let uploadedImage = null;
let analysisResults = null;

// DOM Elements
const imageInput = document.getElementById('image');
const reportTextarea = document.getElementById('report');
const analyzeBtn = document.getElementById('analyzeBtn');
const imagePreview = document.getElementById('imagePreview');
const previewImg = document.getElementById('previewImg');
const removeImageBtn = document.getElementById('removeImage');
const charCount = document.getElementById('charCount');
const resultsSection = document.getElementById('resultsSection');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  setupEventListeners();
  updateCharCount();
  checkFormValidity();
});

// Event Listeners Setup
function setupEventListeners() {
  imageInput.addEventListener('change', handleImageUpload);
  removeImageBtn.addEventListener('click', handleRemoveImage);
  reportTextarea.addEventListener('input', () => {
    updateCharCount();
    checkFormValidity();
  });
  analyzeBtn.addEventListener('click', handleAnalyze);
  
  // View toggle buttons
  document.querySelectorAll('.toggle-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const view = e.target.dataset.view;
      switchView(view);
    });
  });
  
  // Export and new case buttons
  document.getElementById('exportBtn')?.addEventListener('click', exportReport);
  document.getElementById('newCaseBtn')?.addEventListener('click', resetForm);
}

// Image Upload Handling
function handleImageUpload(e) {
  const file = e.target.files[0];
  if (!file) return;
  
  if (!file.type.startsWith('image/')) {
    alert('Please upload a valid image file');
    return;
  }
  
  uploadedImage = file;
  const reader = new FileReader();
  
  reader.onload = (e) => {
    previewImg.src = e.target.result;
    imagePreview.classList.remove('hidden');
    checkFormValidity();
  };
  
  reader.readAsDataURL(file);
}

function handleRemoveImage() {
  uploadedImage = null;
  imageInput.value = '';
  imagePreview.classList.add('hidden');
  previewImg.src = '';
  checkFormValidity();
}

// Form Validation
function checkFormValidity() {
  const hasImage = uploadedImage !== null;
  const hasReport = reportTextarea.value.trim().length > 0;
  analyzeBtn.disabled = !(hasImage && hasReport);
}

function updateCharCount() {
  const count = reportTextarea.value.length;
  charCount.textContent = count.toLocaleString();
}

// Main Analysis Function
async function handleAnalyze() {
  if (!uploadedImage || !reportTextarea.value.trim()) {
    alert('Please provide both image and report');
    return;
  }
  
  // Show loading state
  analyzeBtn.classList.add('loading');
  analyzeBtn.disabled = true;
  
  try {
    const formData = new FormData();
    formData.append('image', uploadedImage);
    formData.append('report', reportTextarea.value);
    
    const response = await fetch('/analyze', {
      method: 'POST',
      body: formData
    });
    
    if (!response.ok) {
      throw new Error('Analysis failed');
    }
    
    const data = await response.json();
    analysisResults = data;
    
    // Display results with animation
    displayResults(data);
    
  } catch (error) {
    console.error('Error:', error);
    alert('Analysis failed. Please try again.');
  } finally {
    analyzeBtn.classList.remove('loading');
    analyzeBtn.disabled = false;
  }
}

// Display Results
function displayResults(data) {
  // Show results section
  resultsSection.classList.remove('hidden');
  
  // Smooth scroll to results
  setTimeout(() => {
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }, 100);
  
  // Display each component
  displayAlertBanner(data);
  displayAgreementScore(data);
  displayAIAnalysis(data.image_analysis);
  displayDoctorAnalysis(data.text_analysis);
  displayDiscrepancies(data.discrepancies);
  displayVisuals(data);
  displayRecommendations(data.recommendation);
}

// Alert Banner
function displayAlertBanner(data) {
  const banner = document.getElementById('alertBanner');
  banner.className = `alert-banner ${data.alert_type}`;
  banner.textContent = data.alert_message;
}

// Agreement Score Display with Animation
function displayAgreementScore(data) {
  const scoreValue = document.getElementById('scoreValue');
  const scoreFill = document.getElementById('scoreFill');
  const statusBadge = document.getElementById('statusBadge');
  const riskLevel = document.getElementById('riskLevel');
  const riskDesc = document.getElementById('riskDesc');
  const riskIcon = document.getElementById('riskIcon');
  const riskIndicator = document.getElementById('riskIndicator');
  
  // Animate score
  animateScore(data.agreement_score);
  
  // Status badge
  statusBadge.textContent = data.status;
  statusBadge.className = `card-badge ${data.status.toLowerCase()}`;
  
  // Risk level
  riskLevel.textContent = `${data.risk_level} Risk`;
  riskDesc.textContent = data.alert_message;
  
  // Risk icon and color
  const riskConfig = {
    'LOW': { icon: '✅', color: 'var(--success)' },
    'MEDIUM': { icon: '⚠️', color: 'var(--warning)' },
    'HIGH': { icon: '🔶', color: 'var(--warning)' },
    'CRITICAL': { icon: '🚨', color: 'var(--critical)' }
  };
  
  const config = riskConfig[data.risk_level] || riskConfig['MEDIUM'];
  riskIcon.textContent = config.icon;
  riskIndicator.style.borderLeft = `4px solid ${config.color}`;
}

function animateScore(targetScore) {
  const scoreValue = document.getElementById('scoreValue');
  const scoreFill = document.getElementById('scoreFill');
  
  // Calculate stroke dash offset
  const circumference = 2 * Math.PI * 90; // radius = 90
  const offset = circumference - (targetScore / 100) * circumference;
  
  // Animate the circle
  setTimeout(() => {
    scoreFill.style.strokeDashoffset = offset;
    
    // Change color based on score
    if (targetScore >= 80) {
      scoreFill.style.stroke = 'var(--success)';
      scoreValue.style.color = 'var(--success)';
    } else if (targetScore >= 60) {
      scoreFill.style.stroke = 'var(--warning)';
      scoreValue.style.color = 'var(--warning)';
    } else {
      scoreFill.style.stroke = 'var(--critical)';
      scoreValue.style.color = 'var(--critical)';
    }
  }, 100);
  
  // Animate number
  animateNumber(scoreValue, 0, targetScore, 1500);
}

function animateNumber(element, start, end, duration) {
  const range = end - start;
  const increment = range / (duration / 16);
  let current = start;
  
  const timer = setInterval(() => {
    current += increment;
    if (current >= end) {
      current = end;
      clearInterval(timer);
    }
    element.textContent = Math.round(current);
  }, 16);
}

// AI Analysis Display
function displayAIAnalysis(data) {
  const aiDiagnosis = document.getElementById('aiDiagnosis');
  const aiConfidence = document.getElementById('aiConfidence');
  const aiConfidenceFill = document.getElementById('aiConfidenceFill');
  const aiFindings = document.getElementById('aiFindings');
  
  aiDiagnosis.textContent = data.prediction;
  aiConfidence.textContent = data.confidence;
  
  // Animate confidence bar
  setTimeout(() => {
    aiConfidenceFill.style.width = `${data.confidence}%`;
  }, 100);
  
  // Display findings
  if (data.detailed_findings && data.detailed_findings.specific_findings) {
    aiFindings.innerHTML = data.detailed_findings.specific_findings.map(finding => `
      <div class="finding-item ${finding.severity}">
        <span class="finding-icon">🔍</span>
        <span class="finding-text">${finding.finding}</span>
        <span class="finding-confidence">${finding.confidence}%</span>
      </div>
    `).join('');
  }
}

// Doctor Report Analysis Display
function displayDoctorAnalysis(data) {
  const doctorDiagnosis = document.getElementById('doctorDiagnosis');
  const doctorConfidence = document.getElementById('doctorConfidence');
  const doctorConfidenceFill = document.getElementById('doctorConfidenceFill');
  const doctorFindings = document.getElementById('doctorFindings');
  
  doctorDiagnosis.textContent = data.text_diagnosis;
  doctorConfidence.textContent = data.confidence;
  
  // Animate confidence bar
  setTimeout(() => {
    doctorConfidenceFill.style.width = `${data.confidence}%`;
  }, 200);
  
  // Display findings from report
  if (data.detailed_findings && data.detailed_findings.specific_findings) {
    doctorFindings.innerHTML = data.detailed_findings.specific_findings.map(finding => `
      <div class="finding-item">
        <span class="finding-icon">📋</span>
        <span class="finding-text">${finding.finding}</span>
      </div>
    `).join('');
  }
}

// Discrepancy Display
function displayDiscrepancies(data) {
  const discrepancySection = document.getElementById('discrepancySection');
  const discrepancyCount = document.getElementById('discrepancyCount');
  const discrepancyList = document.getElementById('discrepancyList');
  const discrepancySummary = document.getElementById('discrepancySummary');
  
  if (!data || data.count === 0) {
    discrepancySection.classList.add('hidden');
    return;
  }
  
  discrepancySection.classList.remove('hidden');
  discrepancyCount.textContent = data.count;
  discrepancySummary.textContent = data.summary;
  
  discrepancyList.innerHTML = data.items.map(item => `
    <div class="discrepancy-item ${item.severity}">
      <div class="discrepancy-header">
        <div class="discrepancy-type">${formatDiscrepancyType(item.type)}</div>
        <div class="severity-badge ${item.severity}">${item.severity}</div>
      </div>
      <div class="discrepancy-desc">${item.description}</div>
      <div class="discrepancy-comparison">
        <div class="comparison-col">
          <div class="comparison-label">🤖 AI Finding</div>
          <div class="comparison-value">${item.ai_finding}</div>
        </div>
        <div class="comparison-col">
          <div class="comparison-label">👨‍⚕️ Report Finding</div>
          <div class="comparison-value">${item.doctor_finding}</div>
        </div>
      </div>
    </div>
  `).join('');
}

function formatDiscrepancyType(type) {
  return type.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
}

// Visual Display
function displayVisuals(data) {
  const gradcamImg = document.getElementById('gradcamImg');
  const originalImg = document.getElementById('originalImg');
  const comparisonOriginal = document.getElementById('comparisonOriginal');
  const comparisonHeatmap = document.getElementById('comparisonHeatmap');
  
  // Load images
  if (data.gradcam_image) {
    gradcamImg.src = data.gradcam_image;
    comparisonHeatmap.src = data.gradcam_image;
  }
  
  if (data.original_image) {
    originalImg.src = data.original_image;
    comparisonOriginal.src = data.original_image;
  }
}

function switchView(viewType) {
  // Update buttons
  document.querySelectorAll('.toggle-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.view === viewType);
  });
  
  // Update views
  document.querySelectorAll('.image-view').forEach(view => {
    view.classList.remove('active');
  });
  
  document.getElementById(`${viewType}View`).classList.add('active');
}

// Recommendations Display
function displayRecommendations(data) {
  const recommendationContent = document.getElementById('recommendationContent');
  
  if (!data) return;
  
  recommendationContent.innerHTML = `
    <div class="recommendation-action">
      <div class="action-type">Recommended Action</div>
      <div class="action-message">${data.message}</div>
      <ul class="next-steps">
        ${data.next_steps.map(step => `<li>${step}</li>`).join('')}
      </ul>
    </div>
  `;
}

// Export Report
function exportReport() {
  if (!analysisResults) return;
  
  const reportContent = generateReportText();
  const blob = new Blob([reportContent], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);
  
  const a = document.createElement('a');
  a.href = url;
  a.download = `MedAI_Analysis_${analysisResults.timestamp}.txt`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

function generateReportText() {
  const data = analysisResults;
  
  return `
╔══════════════════════════════════════════════════════════════╗
║           MEDAI CONSENSUS - ANALYSIS REPORT                  ║
╚══════════════════════════════════════════════════════════════╝

Generated: ${new Date().toLocaleString()}
Case ID: ${data.timestamp}

═══════════════════════════════════════════════════════════════

📊 AGREEMENT ANALYSIS
───────────────────────────────────────────────────────────────
Status:           ${data.status}
Risk Level:       ${data.risk_level}
Agreement Score:  ${data.agreement_score}%
Alert:            ${data.alert_message}

═══════════════════════════════════════════════════════════════

🤖 AI IMAGE ANALYSIS
───────────────────────────────────────────────────────────────
Diagnosis:        ${data.image_analysis.prediction}
Confidence:       ${data.image_analysis.confidence}%

Findings:
${data.image_analysis.detailed_findings?.specific_findings?.map(f => 
  `  • ${f.finding} (${f.confidence}%)`
).join('\n') || '  No specific findings listed'}

═══════════════════════════════════════════════════════════════

👨‍⚕️ CLINICAL REPORT ANALYSIS
───────────────────────────────────────────────────────────────
Diagnosis:        ${data.text_analysis.text_diagnosis}
Confidence:       ${data.text_analysis.confidence}%

═══════════════════════════════════════════════════════════════

⚠️ DISCREPANCIES (${data.discrepancies?.count || 0})
───────────────────────────────────────────────────────────────
${data.discrepancies?.items?.map(d => 
  `
Type:        ${d.type}
Severity:    ${d.severity}
Description: ${d.description}
AI Finding:  ${d.ai_finding}
Report:      ${d.doctor_finding}
`).join('\n') || 'No discrepancies detected'}

═══════════════════════════════════════════════════════════════

💡 RECOMMENDATIONS
───────────────────────────────────────────────────────────────
${data.recommendation?.message}

Next Steps:
${data.recommendation?.next_steps?.map((step, i) => 
  `  ${i + 1}. ${step}`
).join('\n') || ''}

═══════════════════════════════════════════════════════════════

DISCLAIMER: This analysis is for research purposes only and 
should not replace professional medical judgment.

═══════════════════════════════════════════════════════════════
  `.trim();
}

// Reset Form
function resetForm() {
  // Clear inputs
  imageInput.value = '';
  reportTextarea.value = '';
  
  // Reset preview
  uploadedImage = null;
  imagePreview.classList.add('hidden');
  previewImg.src = '';
  
  // Hide results
  resultsSection.classList.add('hidden');
  
  // Reset state
  analysisResults = null;
  
  // Update UI
  updateCharCount();
  checkFormValidity();
  
  // Scroll to top
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Utility Functions
function formatTimestamp(timestamp) {
  const date = new Date(timestamp);
  return date.toLocaleString();
}

function showNotification(message, type = 'info') {
  // Could implement toast notifications here
  console.log(`[${type}] ${message}`);
}