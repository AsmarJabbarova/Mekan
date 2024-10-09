import { Formik, Field, Form, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import './ContactWithUsStyles.css'

interface FormValues {
  name: string;
  email: string;
  phone: string;
  subject: string;
  message: string;
}

const initialValues: FormValues = {
  email: '',
  name: '',
  phone: '',
  subject: '',
  message: '',
};

const validationSchema = Yup.object({
  email: Yup.string()
    .email('Invalid email format')
    .required('Email is required'),

  name: Yup.string()
    .required('Name is required'),

  phone: Yup.string()
    .matches(/^\d+$/, 'Phone must be a number')
    .required('Phone is required'),

  subject: Yup.string()
    .required("Subject is required"),

  message: Yup.string()
    .required("Message is required")
});

const ContactWithUsSection: React.FC = () => {
  const onSubmit = (values: FormValues) => {
    console.log('Form data', values);
  };
    return (
      <div className='contact-with-us-sec'>
        <div className='contact-with-us-inner-right-sec'>
          <div className="contact-with-us-top-sec">
              <div className="contact-with-us-top-inner">
                  Contact with us
              </div>
          </div>
          <div className="contact-top-desc-sec">
            Have questions? Feel free to write us
          </div>
          <div className="contact-desc-sec">
          Man braid hell of edison bulb four brunch subway tile authentic, chillwave put a bird on church-key ramps heirloom. Set perspiciatis unde omnis estenatus voluptatem aperiae.
          </div>
          <div className="contact-social-icons-sec">
            
          </div>
        </div>
        <div className="form-container">
      <Formik
        initialValues={initialValues}
        validationSchema={validationSchema}
        onSubmit={onSubmit}
        validateOnBlur={false} // Disable validation on blur
        validateOnChange={false} // Disable validation on change
      >
        {({ isSubmitting }) => (
          <Form className="form">
            <div className="form-field">
              <Field type="text" id="name" name="name" placeholder="Your Name" />
              <ErrorMessage name="name" component="div" className="error" />
            </div>

            <div className="form-field">
              <Field type="email" id="email" name="email" placeholder="Your Email" />
              <ErrorMessage name="email" component="div" className="error" />
            </div>

            <div className="form-field">
              <Field type="text" id="phone" name="phone" placeholder="Your Phone" />
              <ErrorMessage name="phone" component="div" className="error" />
            </div>

            <div className="form-field">
              <Field type="text" id="subject" name="subject" placeholder="Subject" />
              <ErrorMessage name="subject" component="div" className="error" />
            </div>

            <div className="form-field full-width">
              <Field as="textarea" id="message" name="message" placeholder="Your Message" />
              <ErrorMessage name="message" component="div" className="error" />
            </div>

            <button type="submit" className="submit-button" disabled={isSubmitting}>
              Send Message
            </button>
          </Form>
        )}
      </Formik>
    </div>


      </div>
    );
  }
  
  export default ContactWithUsSection;