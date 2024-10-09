import ContactTopSection from "../components/ContactTopSection/ContactTopSection";
import ContactUsSection from "../components/ContactUsSection/ContactUsSection";
import ContactWithUsSection from "../components/ContactWithUsSection/ContactWithUsSection";
import '../styles/ContactPageStyles.css'

const ContactPage: React.FC = () => {
    return (
      <div>
        <ContactTopSection/>
        <div className="contact-page">
          <ContactUsSection/>
          <ContactWithUsSection/>
        </div>
      </div>
    );
  }
  
  export default ContactPage;