import React from "react";
import { useFormik } from "formik";
import * as Yup from "yup";
import { modelConfigurations } from "../../models/ModelsConfigurations";

interface CreateFormProps {
  modelName: keyof typeof modelConfigurations;
  onSubmit: (formData: Record<string, any>) => void;
  editingItem?: Record<string, any> | null; // Add editingItem prop
}

const CreateForm: React.FC<CreateFormProps> = ({
  modelName,
  onSubmit,
  editingItem,
}) => {
  const modelConfig = modelConfigurations[modelName];

  if (!modelConfig) {
    return <p>Model configuration not found for {modelName}!</p>;
  }

  const initialValues = modelConfig.fields.reduce(
    (acc, field) => ({
      ...acc,
      [field.name]: editingItem?.[field.name] || "", 
    }),
    {}
  );

  const validationSchema = Yup.object(
    modelConfig.fields.reduce((acc, field) => {
      if (field.required) {
        acc[field.name] = Yup.string().required(`${field.label} is required`);
      }
      return acc;
    }, {})
  );

  const formik = useFormik({
    initialValues,
    validationSchema,
    enableReinitialize: true,
    onSubmit: (values) => {
      onSubmit(values);
    },
  });

  return (
    <div className="create-form">
      <h3>{editingItem ? `Edit ${modelName}` : `Create New ${modelName}`}</h3>
      <form onSubmit={formik.handleSubmit}>
        {modelConfig.fields.map((field) => (
          <div key={field.name} className="form-group">
            <label>{field.label}</label>
            <input
              type={field.type}
              name={field.name}
              value={formik.values[field.name]}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
            />
            {formik.touched[field.name] && formik.errors[field.name] && (
              <span className="error">{formik.errors[field.name]}</span>
            )}
          </div>
        ))}
        <div className="form-actions">
          <button type="submit">{editingItem ? "Update" : "Submit"}</button>
        </div>
      </form>
    </div>
  );
};

export default CreateForm;
