import AboutBodySection from "../components/AboutBodySection/AboutBodySection";
import AboutMembersSection from "../components/AboutMembersSection/AboutMembersSection";
import AboutTopSection from "../components/AboutTopSection/AboutTopSection";

const AboutPage: React.FC = () => {
    return (
      <div>
        <AboutTopSection/>
        <AboutBodySection/>
        <AboutMembersSection/>
      </div>
    );
  }
  
  export default AboutPage;