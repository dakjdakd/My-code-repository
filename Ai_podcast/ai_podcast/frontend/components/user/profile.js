// 直接使用 JavaScript 版本，而不是 TypeScript
class UserProfile {
    constructor() {
        this.charts = {
            usageChart: null,
            usageDonut: null,
            dailyUsage: null
        };
        this.init();
        this.setupAvatarUpload();
    }

    initializeCharts() {
        try {
            // 使用趋势图表
            const usageChartEl = document.querySelector("#usageChart");
            if (usageChartEl) {
                this.charts.usageChart = new ApexCharts(usageChartEl, {
                    series: [{
                        name: '使用时长',
                        data: [14, 22, 18, 25, 20, 28, 32]
                    }],
                    chart: {
                        type: 'area',
                        height: 350,
                        background: 'transparent',
                        toolbar: { show: false },
                        fontFamily: 'Montserrat, sans-serif'
                    },
                    colors: ['#a78bfa'],
                    fill: {
                        type: 'gradient',
                        gradient: {
                            shadeIntensity: 1,
                            opacityFrom: 0.7,
                            opacityTo: 0.3,
                            stops: [0, 90, 100]
                        }
                    },
                    dataLabels: {
                        enabled: true,
                        style: {
                            fontSize: '14px',
                            fontWeight: 600,
                            colors: ['#e879f9']
                        },
                        background: {
                            enabled: true,
                            foreColor: '#e879f9',
                            padding: 4,
                            borderRadius: 4,
                            borderWidth: 0,
                            opacity: 0.9,
                            dropShadow: {
                                enabled: true,
                                top: 1,
                                left: 1,
                                blur: 3,
                                color: 'rgba(0, 0, 0, 0.3)',
                                opacity: 0.3
                            }
                        },
                        offsetY: -10
                    },
                    stroke: {
                        curve: 'smooth',
                        width: 3
                    },
                    xaxis: {
                        categories: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
                        labels: {
                            style: {
                                colors: '#e879f9',
                                fontSize: '14px',
                                fontWeight: 600
                            }
                        }
                    },
                    yaxis: {
                        labels: {
                            style: {
                                colors: '#e879f9',
                                fontSize: '14px',
                                fontWeight: 600
                            },
                            formatter: (value) => `${value}分钟`
                        },
                        min: 0,
                        max: 40,
                        tickAmount: 4
                    },
                    grid: {
                        borderColor: 'rgba(255, 255, 255, 0.1)',
                        strokeDashArray: 5
                    },
                    tooltip: {
                        theme: 'dark',
                        style: {
                            fontSize: '14px'
                        },
                        y: {
                            formatter: (value) => `${value} 分钟`
                        }
                    }
                });
                this.charts.usageChart.render();
            }

            // 使用时长分布图表
            const usageDonutEl = document.querySelector("#usageDonut");
            if (usageDonutEl) {
                this.charts.usageDonut = new ApexCharts(usageDonutEl, {
                    series: [65, 35],
                    chart: {
                        type: 'donut',
                        height: 350,
                        background: 'transparent'
                    },
                    colors: ['#a78bfa', '#4f46e5'],
                    labels: ['已使用', '剩余'],
                    plotOptions: {
                        pie: {
                            donut: {
                                size: '75%',
                                labels: {
                                    show: true,
                                    name: {
                                        show: true,
                                        fontSize: '16px',
                                        fontWeight: 600,
                                        color: '#fff',
                                        offsetY: 0
                                    },
                                    value: {
                                        show: false  // 隐藏数值
                                    },
                                    total: {
                                        show: true,
                                        label: '总时长',
                                        fontSize: '16px',
                                        fontWeight: 600,
                                        color: '#fff'
                                    }
                                }
                            }
                        }
                    },
                    legend: {
                        show: true,
                        position: 'right',
                        fontSize: '14px',
                        fontWeight: 600,
                        labels: {
                            colors: '#fff'
                        },
                        markers: {
                            width: 12,
                            height: 12,
                            radius: 6
                        }
                    }
                });
                this.charts.usageDonut.render();
            }

            // 每日使用情况图表
            const dailyUsageEl = document.querySelector("#dailyUsage");
            if (dailyUsageEl) {
                this.charts.dailyUsage = new ApexCharts(dailyUsageEl, {
                    series: [{
                        name: '使用时长',
                        data: [25, 35, 45, 30, 40, 20, 15]
                    }],
                    chart: {
                        type: 'bar',
                        height: 350,
                        background: 'transparent',
                        toolbar: { show: false }
                    },
                    colors: ['#c4b5fd'],
                    fill: {
                        type: 'gradient',
                        gradient: {
                            type: 'vertical',
                            shadeIntensity: 0.2,
                            inverseColors: false,
                            opacityFrom: 1,
                            opacityTo: 0.7,
                            stops: [0, 100],
                            colorStops: [
                                {
                                    offset: 0,
                                    color: '#ddd6fe',
                                    opacity: 1
                                },
                                {
                                    offset: 100,
                                    color: '#c4b5fd',
                                    opacity: 0.7
                                }
                            ]
                        }
                    },
                    plotOptions: {
                        bar: {
                            borderRadius: 8,
                            columnWidth: '60%',
                            dataLabels: {
                                position: 'top'
                            }
                        }
                    },
                    dataLabels: {
                        enabled: true,
                        formatter: function(val) {
                            return val + '分钟';
                        },
                        offsetY: -25,
                        style: {
                            fontSize: '14px',
                            fontWeight: 600,
                            colors: ['#e879f9']
                        },
                        background: {
                            enabled: true,
                            foreColor: '#e879f9',
                            padding: 4,
                            borderRadius: 4,
                            borderWidth: 0,
                            opacity: 0.9,
                            dropShadow: {
                                enabled: true,
                                top: 1,
                                left: 1,
                                blur: 3,
                                color: '#000',
                                opacity: 0.3
                            }
                        }
                    },
                    xaxis: {
                        categories: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
                        labels: {
                            style: {
                                colors: '#e879f9',
                                fontSize: '14px',
                                fontWeight: 600
                            }
                        },
                        axisBorder: {
                            show: false
                        },
                        axisTicks: {
                            show: false
                        }
                    },
                    yaxis: {
                        labels: {
                            style: {
                                colors: '#e879f9',
                                fontSize: '14px',
                                fontWeight: 600
                            },
                            formatter: function(value) {
                                return value + '分钟';
                            }
                        },
                        min: 0,
                        max: 50,
                        tickAmount: 5
                    },
                    grid: {
                        borderColor: 'rgba(255, 255, 255, 0.1)',
                        strokeDashArray: 5,
                        padding: {
                            top: 30
                        }
                    },
                    tooltip: {
                        theme: 'dark',
                        y: {
                            formatter: function(value) {
                                return value + ' 分钟';
                            }
                        }
                    }
                });
                this.charts.dailyUsage.render();
            }
            
        } catch (error) {
            console.error('Error in initializeCharts:', error);
        }
    }

    init() {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.initializeCharts());
        } else {
            this.initializeCharts();
        }
    }

    setupAvatarUpload() {
        const editAvatarBtn = document.querySelector('.edit-avatar');
        const avatarInput = document.createElement('input');
        avatarInput.type = 'file';
        avatarInput.accept = 'image/*';
        avatarInput.style.display = 'none';
        document.body.appendChild(avatarInput);

        // 从localStorage获取保存的头像URL
        const savedAvatarUrl = localStorage.getItem('userAvatar');
        if (savedAvatarUrl) {
            document.querySelector('.avatar').src = savedAvatarUrl;
        }

        editAvatarBtn?.addEventListener('click', () => {
            avatarInput.click();
        });

        avatarInput.addEventListener('change', async (e) => {
            const file = e.target.files[0];
            if (!file) return;

            try {
                console.log('开始上传文件:', file.name);
                const formData = new FormData();
                formData.append('avatar', file);

                const response = await fetch('http://localhost:5000/api/upload-avatar', {
                    method: 'POST',
                    body: formData
                });

                console.log('服务器响应状态:', response.status);
                const responseData = await response.json();
                console.log('服务器响应数据:', responseData);

                if (!response.ok) {
                    throw new Error(responseData.error || '上传失败');
                }

                // 更新头像显示
                const avatarImg = document.querySelector('.avatar');
                avatarImg.src = responseData.avatar_url;
                
                // 保存到localStorage
                localStorage.setItem('userAvatar', responseData.avatar_url);
                
                // 显示成功提示
                this.showNotification('头像更新成功', 'success');

            } catch (error) {
                console.error('上传头像失败:', error);
                this.showNotification(error.message || '上传头像失败，请重试', 'error');
            }
        });
    }

    showNotification(message, type) {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
}

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded, initializing UserProfile...');
    new UserProfile();
}); 