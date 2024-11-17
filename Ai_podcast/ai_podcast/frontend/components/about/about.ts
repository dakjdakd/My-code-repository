export class About {
    private readonly cards: NodeListOf<Element>;
    private readonly observer: IntersectionObserver;

    constructor() {
        this.cards = document.querySelectorAll('.value-card, .team-card');
        this.observer = new IntersectionObserver(this.handleIntersection.bind(this), {
            threshold: 0.1
        });
        this.init();
    }

    private init(): void {
        this.setupAnimations();
        this.setupMap();
    }

    private setupAnimations(): void {
        const sections = document.querySelectorAll('.about-section');
        
        sections.forEach(section => {
            section.classList.add('animate-on-scroll');
            this.observer.observe(section);
        });

        this.cards.forEach(card => {
            card.addEventListener('mouseenter', (e: Event) => this.handleCardHover(e));
            card.addEventListener('mouseleave', (e: Event) => this.handleCardLeave(e));
        });
    }

    private handleIntersection(entries: IntersectionObserverEntry[]): void {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                this.observer.unobserve(entry.target);
            }
        });
    }

    private handleCardHover(e: Event): void {
        const card = e.currentTarget as HTMLElement;
        card.style.transform = 'translateY(-10px)';
        card.style.transition = 'transform 0.3s ease';
    }

    private handleCardLeave(e: Event): void {
        const card = e.currentTarget as HTMLElement;
        card.style.transform = 'translateY(0)';
    }

    private setupMap(): void {
        const mapPlaceholder = document.querySelector('.map-placeholder');
        if (mapPlaceholder) {
            mapPlaceholder.addEventListener('click', () => {
                window.open('https://maps.google.com/?q=北京市海淀区科技园区', '_blank');
            });
        }
    }
}

// 初始化关于页面
new About(); 