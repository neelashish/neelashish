import { JSX } from "react";
import { SubViewNavigation, SubViewParams } from "./AboutView";
import styles from './AboutView.module.css';
import Image from 'next/image';


function ProjectImage(props: { src: string, alt: string, label?: string, labelNumber?: number }) {
  const { src, alt, label, labelNumber } = props;

  return (<>
      <div className={styles['project-image-container']}>
        <Image
          src={src}
          alt={alt}
          fill
          quality={90}
          style={{ objectFit: 'contain' }}
          sizes="400px, 800px, 1024px"
        />
      </div>
      {label && <span className={styles['project-image-label']}><b>Label {labelNumber ?? 1}: </b>{label}</span>}
    </>
  );
}

function ProjectPage(props: { title: string, params: SubViewParams, content: JSX.Element }) {
  const params = props.params;

  function openContactApp() {
    params.manager.open('/Applications/Contact.app');
  }

  function englishContent() {
    const contact = (<>
      <p>If you have any questions or comments, please contact me via the <a onClick={() => openContactApp()} href='#contact'>contact application</a> or shoot me an email at <a href="mailto:neelashish0@gmail.com">neelashish0@gmail.com</a></p>
    </>);

    return { contact };
  }

  const content = englishContent();
  const backToProjects = 'Back to projects';

  return (<>
    <div data-subpage className={styles['subpage']}>
      { SubViewNavigation(params) }
      <div data-subpage-content className={styles['subpage-content']}>
        <h1>{props.title}</h1>
        <button onClick={() => params.changeParent('projects')} className={styles['button-link']}>{backToProjects}</button>
        { props.content }

        <h3>Contact</h3>
        { content.contact }

        <button onClick={() => params.changeParent('projects')} className={styles['button-link']}>{backToProjects}</button>
      </div>
    </div>
  </>);
}


export function ProjectUSMurders(params: SubViewParams) {
  function RenderEnglishContent() {
    return (
      <div>
        <p>This project analyzes murder rates by state in the United States using various data visualizations in R.</p>
        <p>It loads and processes the US murders dataset to generate insights about murder distributions, regional differences, and rate comparisons across different states.</p>
        
        <ProjectImage src="/images/project1.png" alt="Murder Rate Visualizations" label="U.S. Murders Data Analysis Plots" />

        <h3>Technology</h3>
        <p>R (dslabs, base plotting)</p>
        
        <h3>Source Code</h3>
        <p>
          <a target="_blank" rel="noreferrer" href="https://github.com/neelashish/U.S-Murders-Data-analysis-.git">GitHub Repository</a>
        </p>
      </div>
    );
  }
  let content = RenderEnglishContent();

  return ProjectPage({title: 'U.S. Murders Data Analysis', content, params});
}

export function ProjectTempComparison(params: SubViewParams) {
  function RenderEnglishContent() {
    return (
      <div>
        <p>This project compares the average monthly temperatures of Delhi, Mumbai, and New York over a year.</p>
        <p>It uses multi-line plots to demonstrate trends and differences in temperature profiles across geographical zones.</p>

        <ProjectImage src="/images/project2.png" alt="Monthly Temperature Line Plots" label="Monthly Temperature Comparison Line Plots" />

        <h3>Technology</h3>
        <p>R (base plotting)</p>

        <h3>Source Code</h3>
        <p>
          <a target="_blank" rel="noreferrer" href="https://github.com/neelashish/Monthly-Temperature-Comparison.git">GitHub Repository</a>
        </p>
      </div>
    );
  }
  let content = RenderEnglishContent();

  return ProjectPage({title: 'Monthly Temperature Comparison', content, params});
}

export function ProjectNetflixAnalyzer(params: SubViewParams) {
  function RenderEnglishContent() {
    return (
      <div>
        <p>This project analyzes Netflix content data to uncover trends in movies and TV shows available on the platform.</p>
        <p>It explores patterns such as content type distribution (Movies vs. TV Shows), top producing countries, genre frequency, rating distributions, and release year trends — providing insights into how Netflix's catalog has evolved over time.</p>

        <h3>Technology</h3>
        <p>Python (Pandas, Matplotlib, Seaborn)</p>

        <h3>Source Code</h3>
        <p>
          <a target="_blank" rel="noreferrer" href="https://github.com/neelashish/Netflix-Data-analyzer.git">GitHub Repository</a>
        </p>
      </div>
    );
  }
  let content = RenderEnglishContent();

  return ProjectPage({title: 'Netflix Data Analyzer', content, params});
}
