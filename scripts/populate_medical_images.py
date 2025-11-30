"""
Populate the patient database with sample medical imaging data.
Downloads medical imaging datasets and stores them using patient_db_tool.
"""
import importlib.util
import pathlib
import sys
import base64
import logging
from typing import List, Dict, Any
import os

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PopulateMedicalImages")

# Import patient_db_tool
mod_path = pathlib.Path(__file__).resolve().parents[1] / "medagent" / "patient_db_tool.py"
spec = importlib.util.spec_from_file_location("patient_db_tool", str(mod_path))
patient_db_tool = importlib.util.module_from_spec(spec)
sys.modules["patient_db_tool"] = patient_db_tool
spec.loader.exec_module(patient_db_tool)

store_patient_file_in_db = patient_db_tool.store_patient_file_in_db
store_patient_data_in_db = patient_db_tool.store_patient_data_in_db
get_patient_file_from_db = patient_db_tool.get_patient_file_from_db


def download_mimic_cxr_sample():
    """Download sample chest X-rays from MIMIC-CXR dataset via Kaggle."""
    try:
        import kagglehub
        logger.info("Downloading MIMIC-CXR sample images from Kaggle...")
        
        # Download the dataset
        path = kagglehub.dataset_download("montassarba/mimic-iv-clinical-database-demo-2-2")
        logger.info(f"Dataset downloaded to: {path}")
        return path
    except Exception as e:
        logger.warning(f"Could not download MIMIC-CXR: {e}")
        return None


def create_sample_images():
    """Create sample medical images for demonstration."""
    import numpy as np
    from PIL import Image
    import io
    
    samples = []
    
    # Sample 1: Chest X-ray (simulated)
    logger.info("Creating simulated chest X-ray...")
    img_cxr = np.random.randint(0, 256, (512, 512), dtype=np.uint8)
    # Add some structure (simulated lungs)
    img_cxr[150:400, 100:200] = np.minimum(img_cxr[150:400, 100:200] + 50, 255)
    img_cxr[150:400, 300:400] = np.minimum(img_cxr[150:400, 300:400] + 50, 255)
    
    img_obj = Image.fromarray(img_cxr, mode='L')
    buf = io.BytesIO()
    img_obj.save(buf, format='PNG')
    samples.append({
        'patient_id': 'DEMO-001',
        'type': 'chest_xray',
        'data': buf.getvalue(),
        'filename': 'chest_xray_pa.png',
        'mime_type': 'image/png',
        'description': '45-year-old male with persistent cough',
        'metadata': {'age': 45, 'sex': 'male', 'study': 'chest_xray_pa'}
    })
    
    # Sample 2: CT scan slice (simulated)
    logger.info("Creating simulated CT scan slice...")
    img_ct = np.random.randint(0, 256, (256, 256), dtype=np.uint8)
    # Add some structure
    img_ct[80:180, 80:180] = np.minimum(img_ct[80:180, 80:180] + 80, 255)
    
    img_obj = Image.fromarray(img_ct, mode='L')
    buf = io.BytesIO()
    img_obj.save(buf, format='PNG')
    samples.append({
        'patient_id': 'DEMO-002',
        'type': 'CT',
        'data': buf.getvalue(),
        'filename': 'ct_chest_slice.png',
        'mime_type': 'image/png',
        'description': '62-year-old female with suspected pneumonia',
        'metadata': {'age': 62, 'sex': 'female', 'study': 'ct_chest'}
    })
    
    # Sample 3: MRI brain slice (simulated)
    logger.info("Creating simulated MRI brain slice...")
    img_mri = np.random.randint(50, 200, (256, 256), dtype=np.uint8)
    # Add brain-like structure
    center = 128
    radius = 80
    y, x = np.ogrid[:256, :256]
    mask = (x - center)**2 + (y - center)**2 <= radius**2
    img_mri[mask] = np.minimum(img_mri[mask] + 50, 255)
    
    img_obj = Image.fromarray(img_mri, mode='L')
    buf = io.BytesIO()
    img_obj.save(buf, format='PNG')
    samples.append({
        'patient_id': 'DEMO-003',
        'type': 'MRI',
        'data': buf.getvalue(),
        'filename': 'mri_brain_t1.png',
        'mime_type': 'image/png',
        'description': '38-year-old male with headaches',
        'metadata': {'age': 38, 'sex': 'male', 'study': 'mri_brain_t1'}
    })
    
    return samples


def populate_database():
    """Main function to populate the database."""
    logger.info("Starting database population...")
    
    # Try to download real data first
    dataset_path = download_mimic_cxr_sample()
    
    # Create simulated samples
    samples = create_sample_images()
    
    # Store in database
    for sample in samples:
        logger.info(f"Storing {sample['type']} for patient {sample['patient_id']}...")
        
        # Store patient description
        store_patient_data_in_db(
            patient_id=sample['patient_id'],
            description=sample['description'],
            metadata=sample['metadata']
        )
        
        # Store image file
        store_patient_file_in_db(
            patient_id=sample['patient_id'],
            file_type=sample['type'],
            file_data=sample['data'],
            filename=sample['filename'],
            mime_type=sample['mime_type']
        )
    
    logger.info("✅ Database population complete!")
    
    # Verify
    logger.info("\nVerifying stored data...")
    for sample in samples:
        files = get_patient_file_from_db(sample['patient_id'], sample['type'])
        if files:
            logger.info(f"  ✓ {sample['patient_id']}: {len(files)} file(s), "
                       f"size: {len(files[0]['data'])} bytes")
        else:
            logger.warning(f"  ✗ {sample['patient_id']}: No files found")
    
    logger.info(f"\n📁 Database location: {patient_db_tool.DB_PATH}")


if __name__ == "__main__":
    try:
        populate_database()
    except KeyboardInterrupt:
        logger.info("\n❌ Interrupted by user")
    except Exception as e:
        logger.error(f"❌ Error: {e}", exc_info=True)
