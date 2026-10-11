import { WindowProps } from '@/components/WindowManagement/WindowCompositor';
import { JSX, useEffect, useRef, useState } from 'react';
import Image from 'next/image';
import styles from './AboutView.module.css';
import { BaseApplicationManager } from '../ApplicationManager';
import { useTranslation } from 'react-i18next';
import { TFunction } from 'i18next';
import { ProjectUSMurders, ProjectTempComparison, ProjectNetflixAnalyzer } from './Projects';
import { ScreenResolution } from '@/apis/Screen/ScreenService';

type SubView = (
  'home' |
  'about' |
  'experience' |
  'projects' |
  'project-us-murders' |
  'project-temp-comparison' |
  'project-netflix-analyzer' |
  'contact'
);

export type SubViewParams = {
  needsMobileView: boolean,
  manager: BaseApplicationManager,
  changeParent: (view: SubView) => void,
  translate: TFunction,
  language: string
}

function Contact(props: { manager: BaseApplicationManager, language: string }): JSX.Element {
  function openContactApp() {
    props.manager.open('/Applications/Contact.app');
  }

  return (
    <>
      <p>If you have any questions or comments, please contact me via the <a onClick={() => openContactApp()} href='#contact'>contact application</a> or shoot me an email at <a href="mailto:hello@neelashish.dev">hello@neelashish.dev</a></p>
    </>
  );
}

// CV download component removed

function HomeSubView(params: SubViewParams) {
  const t = params.translate;

  const mobileClass = params.needsMobileView ? styles['mobile'] : '';

  return (<>
    <div className={styles['subpage-home']}>
      <h1 className={styles['home-title']}>Neelashish</h1>
      <h3 className={styles['home-subtitle']}>AI & Data Science Student</h3>

      <div className={styles['home-button-container']}>
        <button className={`${styles['home-button']} system-button ${mobileClass}`} onClick={() => params.changeParent('about')}>{t("about.navigation.about")}</button>
        <button className={`${styles['home-button']} system-button ${mobileClass}`} onClick={() => params.changeParent('experience')}>{t("about.navigation.experience")}</button>
        <button className={`${styles['home-button']} system-button ${mobileClass}`} onClick={() => params.changeParent('projects')}>{t("about.navigation.projects")}</button>
        <button className={`${styles['home-button']} system-button ${mobileClass}`} onClick={() => params.changeParent('contact')}>{t("about.navigation.contact")}</button>
      </div>
    </div>
  </>)
}

export function SubViewNavigation(params: SubViewParams) {
  const t = params.translate;

  const mobileClass = params.needsMobileView ? styles['mobile'] : '';

  return (<>
    <div className={styles['navigation']}>
      <div>
        <span className={styles['logo-part']}>Neelashish</span>
      </div>

      <div className={`${styles['navigation-button-container']} ${mobileClass}`}>
        <button className='system-button' onClick={() => params.changeParent('home')}>{t("about.navigation.home")}</button>
        <button className='system-button' onClick={() => params.changeParent('about')}>{t("about.navigation.about")}</button>
        <button className='system-button' onClick={() => params.changeParent('experience')}>{t("about.navigation.experience")}</button>
        <button className='system-button' onClick={() => params.changeParent('projects')}>{t("about.navigation.projects")}</button>
        <button className='system-button' onClick={() => params.changeParent('contact')}>{t("about.navigation.contact")}</button>
      </div>
    </div>
  </>)
}

function AboutSubView(params: SubViewParams) {
  function openContactApp() {
    params.manager.open('/Applications/Contact.app');
  }

  function ImageOfMyself() {
    const text = 'neelashish';

    return (<>
      <div className={styles['image-container']}>
        <img draggable={false} src="/images/me.jpg" alt="Image of myself" />
        <span>{text}</span>
      </div>
    </>);
  }


  function RenderEnglishContent() {
    return (
      <div>
        <h1 className={styles['page-h1']}>Welcome</h1>

        <p>
          I’m Neelashish, a 2nd-year B.Tech student in Artificial Intelligence and Data Science.
        </p>

        <p>Thanks for taking the time to explore my portfolio. I hope you enjoy it as much as I did customizing and setting it up. If you have any questions or comments, please contact me via the <a onClick={() => openContactApp()} href='#contact'>contact application</a> or shoot me an email at <a href="mailto:neelashish0@gmail.com">neelashish0@gmail.com</a>.</p>

        <h2>About me</h2>

        <ImageOfMyself/>

        <p>My journey into technology began with a strong interest in how data and artificial intelligence are shaping our world. Starting my B.Tech in AI & Data Science in August 2025, I decided to dedicate myself to building a strong foundation in core areas: mathematics, statistics, machine learning, artificial intelligence, and open-source software development.</p>

        <p>Currently, I am working hard on strengthening my programming capabilities. R is my strongest language so far, where I have mastered core programming concepts like custom functions, loops, apply-family functional programming, and key data structures such as data frames, matrices, and vectors. I have also gotten deep into the Tidyverse ecosystem, including data manipulation with dplyr and visualization with ggplot2.</p>

        <p>In addition to R, I am actively building my foundation in Python, transitioning toward core libraries like NumPy, Pandas, Matplotlib, and Scikit-Learn to expand my machine learning toolkit.</p>

        <p>I believe that a great data scientist needs a solid mathematical foundation, which is why I have been studying Linear Algebra (following MIT 18.06), covering topics like matrix operations, inverse matrices, Gaussian elimination, and introduction to vector spaces. I also enjoy learning about text processing, character encoding (ASCII, Unicode), and practicing prompt engineering to interact effectively with large language models.</p>

        <h2>Hobbies & Interests</h2>

        <p>When I am not coding or studying mathematics, I love exploring open-source repositories on GitHub, configuring my development environment in VS Code, and reading about the latest breakthroughs in AI research. I also enjoy building my online presence and sharing my learning journey with other developers.</p>
      </div>
    );
  }

  return (<>
    <div data-subpage className={styles['subpage']}>
      { SubViewNavigation(params) }
      <div data-subpage-content className={styles['subpage-content']}>
        { RenderEnglishContent() }
      </div>
    </div>
  </>);
}

function ExperienceSubView(params: SubViewParams) {
  const t = params.translate;

  function englishContent() {
    return (
      <div>
        <p>As a 1st-year B.Tech student in Artificial Intelligence & Data Science, my experience is centered around rigorous academic study, self-driven research, and hands-on foundational development in programming, mathematics, and open-source tools.</p>

        <h3>Academic & Self-Study Focus</h3>
        <p>
          <b>Linear Algebra</b>: Mastered solving systems of equations, matrix operations, matrix multiplication, inverse matrices, Gaussian elimination, row operations, and vector spaces.<br/>
          <b>AI Skills</b>: Completed <i>ChatGPT Prompt Engineering for Developers</i>. Learned prompt design, role prompting, few-shot prompting, structured prompting, and iterative refinement.
        </p>

        <h3>Programming & Data Analysis Exposure</h3>
        <p>
          <b>R Programming</b>: Strong foundations in variables, data types, vectors, functions, custom functions, conditional statements, loops, and functional programming (apply, lapply, sapply). Competent with data manipulation using the Tidyverse ecosystem (dplyr, ggplot2, readr, tidyr, stringr, forcats).<br/>
          <b>Python</b>: Actively learning and transitioning to Python for machine learning foundations (NumPy, Pandas, Matplotlib, Scikit-Learn).
        </p>

        <h3>Tools & Workflows</h3>
        <p>
          <b>VS Code</b>: Writing R/Python code, running scripts, and managing project structure.<br/>
          <b>GitHub</b>: Preparing for open-source contributions, mastering basic git workflow and repository management.
        </p>
      </div>
    );
  }

  const content = englishContent();

  return (<>
    <div data-subpage className={styles['subpage']}>
      { SubViewNavigation(params) }
      <div data-subpage-content className={styles['subpage-content']}>
        <h1 className={styles['page-h1']}>{t("about.navigation.experience")}</h1>

        <h2>2025 - Present - B.Tech Student (AI & Data Science)</h2>
        { content }
      </div>
    </div>
  </>);
}

function ProjectsSubView(params: SubViewParams) {
  const t = params.translate;

  return (<>
    <div data-subpage className={styles['subpage']}>
      { SubViewNavigation(params) }
      <div data-subpage-content className={styles['subpage-content']}>
        <h1 className={styles['page-h1']}>My Projects</h1>
        <p style={{ marginBottom: '1rem' }}>Mini data science projects built with R</p>
        
        <ul className={styles['project-list']} style={{ listStyle: 'none', padding: 0, margin: 0, display: 'flex', flexDirection: 'column', gap: '10px' }}>
          <li>
            <button className={styles['project-button']} onClick={() => params.changeParent('project-us-murders')} style={{ width: '100%', display: 'block' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <Image src="/icons/skills-icon.png" alt="Project Icon" width={32} height={32} />
                <div style={{ textAlign: 'left' }}>
                  <span style={{ fontWeight: 'bold', display: 'block' }}>Project 1: U.S. Murders Data Analysis</span>
                  <span style={{ fontSize: '0.85em', color: '#555' }}>Tech Used: R (dslabs, base plotting)</span>
                </div>
              </div>
            </button>
          </li>
          <li>
            <button className={styles['project-button']} onClick={() => params.changeParent('project-temp-comparison')} style={{ width: '100%', display: 'block' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <Image src="/icons/skills-icon.png" alt="Project Icon" width={32} height={32} />
                <div style={{ textAlign: 'left' }}>
                  <span style={{ fontWeight: 'bold', display: 'block' }}>Project 2: Monthly Temperature Comparison</span>
                  <span style={{ fontSize: '0.85em', color: '#555' }}>Tech Used: R (base plotting)</span>
                </div>
              </div>
            </button>
          </li>
          <li>
            <button className={styles['project-button']} onClick={() => params.changeParent('project-netflix-analyzer')} style={{ width: '100%', display: 'block' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <Image src="/icons/skills-icon.png" alt="Project Icon" width={32} height={32} />
                <div style={{ textAlign: 'left' }}>
                  <span style={{ fontWeight: 'bold', display: 'block' }}>Project 3: Netflix Data Analyzer</span>
                  <span style={{ fontSize: '0.85em', color: '#555' }}>Tech Used: Python (Pandas, Matplotlib, Seaborn)</span>
                </div>
              </div>
            </button>
          </li>
        </ul>
      </div>
    </div>
  </>);
}

function RenderSubView(view: SubView, params: SubViewParams): JSX.Element {
  switch (view) {
    case 'home': return HomeSubView(params);
    case 'about': return AboutSubView(params);
    case 'experience': return ExperienceSubView(params);
    case 'projects': return ProjectsSubView(params);
    case 'project-us-murders': return ProjectUSMurders(params);
    case 'project-temp-comparison': return ProjectTempComparison(params);
    case 'project-netflix-analyzer': return ProjectNetflixAnalyzer(params);
    case 'contact': return (<Contact manager={params.manager} language={params.language} />);
  }
  
  return <></>;
}

export default function AboutApplicationView(props: WindowProps) {
  const { application, windowContext } = props;

  const [subView, setSubView] = useState<SubView>('home');
  const [needsMobileView, setNeedsMobileView] = useState<boolean>(false);
  const { t, i18n } = useTranslation("common");

  const apis = application.apis;

  const contentParent = useRef<HTMLDivElement>(null);

  function resetSubPageScroll() {
    if (!contentParent.current) { return; }

    const subViewParent = contentParent.current;
    const subViewParentChildren = Array.from(subViewParent.children);

    const subView = subViewParentChildren.find(x => x.hasAttribute('data-subpage'));
    if (!subView) { return; }

    const subViewChildren = Array.from(subView.children);

    const contentView = subViewChildren.find(x => x.hasAttribute('data-subpage-content'));

    if (!contentView) { return; }
    contentView.scrollTop = 0;
  }

  function onScreenChangeListener(resolution: ScreenResolution): void {
    setNeedsMobileView(resolution.isMobileDevice());
  }

  useEffect(() => {
    const unsubscribe = apis.screen.subscribe(onScreenChangeListener);

    const resolution = apis.screen.getResolution();
    if (resolution) { onScreenChangeListener(resolution); }

    return () => {
      unsubscribe();
    }
  }, []);

  useEffect(() => {
    resetSubPageScroll();
  }, [subView]);

  function changeParent(view: SubView) {
    if (view === 'contact') {
      application.on({ kind: 'about-open-contact-event' }, windowContext);
      return;
    }

    setSubView(view);
  }

  return (
    <div className="content-outer">
      <div className="content">
        <div className='content-inner' ref={contentParent}>
          { RenderSubView(subView,
            {
              needsMobileView,
              manager: application.manager,
              changeParent,
              translate: t,
              language: i18n.language
            }
          ) }
        </div>
      </div>
    </div>
  )
}