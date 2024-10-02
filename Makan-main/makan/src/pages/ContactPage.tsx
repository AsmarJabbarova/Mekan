import ContactTopSection from "../components/ContactTopSection/ContactTopSection";
import ContactUsSection from "../components/ContactUsSection/ContactUsSection";
import ContactWithUsSection from "../components/ContactWithUsSection/ContactWithUsSection";

const ContactPage: React.FC = () => {
    return (
      <div>
        <ContactTopSection/>
        <ContactUsSection/>
        <ContactWithUsSection/>
      </div>
    );
  }
  
  export default ContactPage;