"""
View medical images stored in the patient database.
"""
import importlib.util
import pathlib
import sys
import logging
from PIL import Image
import io

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ViewMedicalImages")

# Import patient_db_tool
mod_path = pathlib.Path(__file__).resolve().parents[1] / "medagent" / "patient_db_tool.py"
spec = importlib.util.spec_from_file_location("patient_db_tool", str(mod_path))
patient_db_tool = importlib.util.module_from_spec(spec)
sys.modules["patient_db_tool"] = patient_db_tool
spec.loader.exec_module(patient_db_tool)

get_patient_file_from_db = patient_db_tool.get_patient_file_from_db
get_patient_data_from_db = patient_db_tool.get_patient_data_from_db

# Import database connection to list all patients
import sqlite3

def list_all_patients():
    """List all patients in the database."""
    conn = sqlite3.connect(patient_db_tool.DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT patient_id, description FROM patient_data ORDER BY patient_id")
    patients = cursor.fetchall()
    conn.close()
    return patients

def view_patient_images(patient_id: str, save_to_disk: bool = True):
    """View and optionally save images for a specific patient."""
    logger.info(f"\n{'='*60}")
    logger.info(f"Patient ID: {patient_id}")
    logger.info(f"{'='*60}")
    
    # Get patient data
    patient_data = get_patient_data_from_db(patient_id)
    if patient_data:
        logger.info(f"Description: {patient_data.get('description', 'N/A')}")
        if patient_data.get('metadata'):
            logger.info(f"Metadata: {patient_data['metadata']}")
    
    # Get all files for this patient
    files = get_patient_file_from_db(patient_id)
    
    if not files:
        logger.warning(f"  No files found for patient {patient_id}")
        return
    
    logger.info(f"\nFound {len(files)} file(s):")
    
    for i, file_data in enumerate(files):
        logger.info(f"\n  File #{i+1}:")
        logger.info(f"    Type: {file_data.get('type', 'N/A')}")
        logger.info(f"    Filename: {file_data.get('filename', 'N/A')}")
        logger.info(f"    MIME Type: {file_data.get('mime_type', 'N/A')}")
        logger.info(f"    Size: {len(file_data['data'])} bytes")
        logger.info(f"    Created: {file_data.get('created_at', 'N/A')}")
        
        if save_to_disk and file_data['data']:
            # Save to disk
            filename = file_data.get('filename', f"{patient_id}_{i}.png")
            output_path = f"output_{patient_id}_{filename}"
            
            try:
                with open(output_path, 'wb') as f:
                    f.write(file_data['data'])
                logger.info(f"    💾 Saved to: {output_path}")
                
                # Try to display image info
                try:
                    img = Image.open(io.BytesIO(file_data['data']))
                    logger.info(f"    📊 Image: {img.format} {img.size[0]}x{img.size[1]} {img.mode}")
                except:
                    pass
                    
            except Exception as e:
                logger.error(f"    ❌ Failed to save: {e}")

def main():
    """Main function to view all medical images."""
    logger.info("🏥 Medical Image Database Viewer")
    logger.info("="*60)
    
    # List all patients
    patients = list_all_patients()
    
    if not patients:
        logger.warning("No patients found in database.")
        return
    
    logger.info(f"\nFound {len(patients)} patient(s):\n")
    for patient_id, description in patients:
        logger.info(f"  • {patient_id}: {description or 'No description'}")
    
    # View each patient's images
    logger.info("\n" + "="*60)
    logger.info("Patient Image Details:")
    logger.info("="*60)
    
    for patient_id, _ in patients:
        view_patient_images(patient_id, save_to_disk=True)
    
    logger.info(f"\n{'='*60}")
    logger.info("✅ Complete! Check the current directory for exported images.")
    logger.info(f"{'='*60}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"❌ Error: {e}", exc_info=True)
