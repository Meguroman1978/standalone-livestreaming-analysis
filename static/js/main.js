// Global variables
let sessionId = null;

// DOM Elements
const videoFileInput = document.getElementById('videoFile');
const dataFileInput = document.getElementById('dataFile');
const commentsFileInput = document.getElementById('commentsFile');

const videoFileName = document.getElementById('videoFileName');
const dataFileName = document.getElementById('dataFileName');
const commentsFileName = document.getElementById('commentsFileName');

const uploadBtn = document.getElementById('uploadBtn');
const uploadProgress = document.getElementById('uploadProgress');
const uploadProgressBar = document.getElementById('uploadProgressBar');
const uploadProgressText = document.getElementById('uploadProgressText');

const uploadSection = document.getElementById('uploadSection');
const analysisSection = document.getElementById('analysisSection');
const reportSection = document.getElementById('reportSection');

const analyzeBtn = document.getElementById('analyzeBtn');
const analysisProgress = document.getElementById('analysisProgress');
const analysisProgressText = document.getElementById('analysisProgressText');

const errorMessage = document.getElementById('errorMessage');
const errorText = document.getElementById('errorText');

const newAnalysisBtn = document.getElementById('newAnalysisBtn');

// File input event listeners
videoFileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        videoFileName.textContent = file.name;
        checkAllFilesSelected();
    }
});

dataFileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        dataFileName.textContent = file.name;
        checkAllFilesSelected();
    }
});

commentsFileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        commentsFileName.textContent = file.name;
        checkAllFilesSelected();
    }
});

// Check if all files are selected
function checkAllFilesSelected() {
    const allSelected = videoFileInput.files.length > 0 && 
                       dataFileInput.files.length > 0 && 
                       commentsFileInput.files.length > 0;
    
    uploadBtn.disabled = !allSelected;
}

// Upload button click handler
uploadBtn.addEventListener('click', async () => {
    uploadBtn.disabled = true;
    uploadProgress.style.display = 'block';
    hideError();
    
    const formData = new FormData();
    formData.append('video', videoFileInput.files[0]);
    formData.append('data', dataFileInput.files[0]);
    formData.append('comments', commentsFileInput.files[0]);
    
    try {
        uploadProgressBar.style.width = '30%';
        uploadProgressText.textContent = 'ファイルをアップロード中...';
        
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (response.ok && result.success) {
            uploadProgressBar.style.width = '100%';
            uploadProgressText.textContent = 'アップロード完了!';
            
            sessionId = result.session_id;
            
            // Show analysis section
            setTimeout(() => {
                analysisSection.style.display = 'block';
                analysisSection.scrollIntoView({ behavior: 'smooth' });
            }, 500);
        } else {
            throw new Error(result.error || 'アップロードに失敗しました');
        }
    } catch (error) {
        showError(error.message);
        uploadBtn.disabled = false;
        uploadProgress.style.display = 'none';
    }
});

// Analyze button click handler
analyzeBtn.addEventListener('click', async () => {
    analyzeBtn.disabled = true;
    analysisProgress.style.display = 'block';
    hideError();
    
    try {
        analysisProgressText.textContent = '動画を分析中... (1/4)';
        
        const response = await fetch(`/api/analyze/${sessionId}`, {
            method: 'POST'
        });
        
        // Simulate progress updates (since actual analysis takes time)
        let progressInterval = setInterval(() => {
            const currentText = analysisProgressText.textContent;
            if (currentText.includes('(1/4)')) {
                analysisProgressText.textContent = 'データを分析中... (2/4)';
            } else if (currentText.includes('(2/4)')) {
                analysisProgressText.textContent = 'コメントを分類中... (3/4)';
            } else if (currentText.includes('(3/4)')) {
                analysisProgressText.textContent = 'レポートを生成中... (4/4)';
            }
        }, 3000);
        
        const result = await response.json();
        clearInterval(progressInterval);
        
        if (response.ok && result.success) {
            analysisProgressText.textContent = '分析完了!';
            
            // Display report
            setTimeout(() => {
                displayReport(result.report_data, result.session_id);
                reportSection.style.display = 'block';
                reportSection.scrollIntoView({ behavior: 'smooth' });
            }, 500);
        } else {
            throw new Error(result.error || '分析に失敗しました');
        }
    } catch (error) {
        showError(error.message);
        analyzeBtn.disabled = false;
        analysisProgress.style.display = 'none';
    }
});

// Display report
function displayReport(reportData, sessionId) {
    // Display summary stats
    displaySummaryStats(reportData.summary_stats);
    
    // Display charts
    displayCharts(reportData.charts, sessionId);
    
    // Display peak analysis
    displayPeakAnalysis(reportData.peak_analysis);
    
    // Display comment analysis
    displayCommentAnalysis(reportData.comment_analysis);
    
    // Display recommendations
    displayRecommendations(reportData.recommendations);
}

// Display summary statistics
function displaySummaryStats(stats) {
    const statsGrid = document.getElementById('statsGrid');
    statsGrid.innerHTML = '';
    
    const statCards = [
        { label: '最大同時視聴者数', value: stats.max_viewers || 0, icon: '👥' },
        { label: '平均視聴者数', value: Math.round(stats.avg_viewers || 0), icon: '📊' },
        { label: '合計いいね数', value: stats.total_likes || 0, icon: '❤️' },
        { label: '合計コメント数', value: stats.total_comments_actual || stats.total_comments_metric || 0, icon: '💬' },
        { label: '合計クリック数', value: stats.total_clicks || 0, icon: '🖱️' }
    ];
    
    statCards.forEach(stat => {
        const card = document.createElement('div');
        card.className = 'stat-card';
        card.innerHTML = `
            <h4>${stat.icon} ${stat.label}</h4>
            <div class="stat-value">${stat.value.toLocaleString()}</div>
        `;
        statsGrid.appendChild(card);
    });
}

// Display charts
function displayCharts(charts, sessionId) {
    if (charts.timeline) {
        const timelineChart = document.getElementById('timelineChart');
        timelineChart.src = `/static/uploads/${sessionId}/${charts.timeline}`;
    }
    
    if (charts.comment_pie) {
        const commentPieChart = document.getElementById('commentPieChart');
        commentPieChart.src = `/static/uploads/${sessionId}/${charts.comment_pie}`;
    }
}

// Display peak analysis
function displayPeakAnalysis(peakAnalysis) {
    const peakAnalysisContent = document.getElementById('peakAnalysisContent');
    peakAnalysisContent.innerHTML = '';
    
    const metrics = {
        'viewers': { title: '👥 同時視聴ユーザー数', color: '#2196F3' },
        'clicks': { title: '🖱️ 商品クリック数', color: '#FF9800' },
        'comments': { title: '💬 チャット数', color: '#4CAF50' },
        'likes': { title: '❤️ いいね数', color: '#E91E63' }
    };
    
    for (const [metric, data] of Object.entries(peakAnalysis)) {
        if (data && data.length > 0) {
            const metricSection = document.createElement('div');
            metricSection.className = 'metric-section';
            
            const metricInfo = metrics[metric] || { title: metric, color: '#667eea' };
            
            metricSection.innerHTML = `<h4>${metricInfo.title}</h4>`;
            
            data.forEach(peak => {
                const peakItem = document.createElement('div');
                peakItem.className = 'peak-item';
                peakItem.innerHTML = `
                    <strong>[${peak.minute}分目]</strong> 
                    値: ${Math.round(peak.value).toLocaleString()} 
                    (増加: +${Math.round(peak.increase).toLocaleString()})
                    <br>
                    <em>📝 ${peak.event_description}</em>
                `;
                metricSection.appendChild(peakItem);
            });
            
            peakAnalysisContent.appendChild(metricSection);
        }
    }
    
    if (peakAnalysisContent.innerHTML === '') {
        peakAnalysisContent.innerHTML = '<p>ピークデータがありません</p>';
    }
}

// Display comment analysis
function displayCommentAnalysis(commentAnalysis) {
    const categoryDetails = document.getElementById('commentCategoryDetails');
    categoryDetails.innerHTML = '';
    
    const categories = commentAnalysis.categories;
    const examples = commentAnalysis.examples;
    
    for (const [category, count] of Object.entries(categories)) {
        const categoryItem = document.createElement('div');
        categoryItem.className = 'category-item';
        
        const categoryExamples = examples[category] || [];
        const examplesHtml = categoryExamples.length > 0 
            ? `<div class="category-examples">
                <strong>例:</strong><br>
                ${categoryExamples.slice(0, 3).map(ex => `• ${ex}`).join('<br>')}
               </div>`
            : '';
        
        categoryItem.innerHTML = `
            <h5>${category}</h5>
            <div class="count">${count}件</div>
            ${examplesHtml}
        `;
        
        categoryDetails.appendChild(categoryItem);
    }
}

// Display recommendations
function displayRecommendations(recommendations) {
    const goodPointsList = document.getElementById('goodPointsList');
    const improvementsList = document.getElementById('improvementsList');
    const nextActionsList = document.getElementById('nextActionsList');
    
    // Good points
    goodPointsList.innerHTML = '';
    recommendations.good_points.forEach(point => {
        const li = document.createElement('li');
        li.textContent = point;
        goodPointsList.appendChild(li);
    });
    
    if (recommendations.good_points.length === 0) {
        goodPointsList.innerHTML = '<li>データ不足のため、評価できません</li>';
    }
    
    // Improvements
    improvementsList.innerHTML = '';
    recommendations.improvements.forEach(improvement => {
        const li = document.createElement('li');
        li.textContent = improvement;
        improvementsList.appendChild(li);
    });
    
    if (recommendations.improvements.length === 0) {
        improvementsList.innerHTML = '<li>現時点で大きな改善点は見つかりませんでした</li>';
    }
    
    // Next actions
    nextActionsList.innerHTML = '';
    recommendations.next_actions.forEach(action => {
        const li = document.createElement('li');
        li.textContent = action;
        nextActionsList.appendChild(li);
    });
}

// New analysis button
newAnalysisBtn.addEventListener('click', () => {
    location.reload();
});

// Error handling
function showError(message) {
    errorText.textContent = message;
    errorMessage.style.display = 'flex';
    errorMessage.scrollIntoView({ behavior: 'smooth' });
}

function hideError() {
    errorMessage.style.display = 'none';
}
