Last Updated: 2024/05/26

# Stellaris-STED Confocal Microscope Instructions Manual

## Starting the System

1. **Power On the Controller**:
   - Turn on the power switch on the left side.
   - Turn on the laser switch.
   - Turn the key to the "on" position.

2. **Log In to the Booking System**:
   - Use your credentials:
     - **Username**: Your email address.
     - **Password**: Your email address password.
   - Verify that your booking is approved and not pending. Contact a facility member if your status is pending.
   - Click "Log In" and then click "Activate Service."

## Configuring the Microscope

1. **Select Configuration**:
   - After logging in, wait for the dialogue box to appear.
   - In the "Configuration" field, choose: **Machine**.
   - In the "Microscope" field, choose: **DMI8**.
   - Click "OK."

2. **Motorized Stage Setup**:
   - When prompted about the motorized stage, click "Yes" to enable X & Y movement.

3. **Software Interface**:
   - The interface will load in about 1-2 minutes.
   - The interface is divided into widgets:
     - **Left Side Widgets**: Scan mode and Z stack settings.
     - **Right Side Widgets**: Objective selection, laser, and detectors settings.

## Setting Up for Imaging

1. **Verify Objective Magnification**:
   - Ensure the microscope is set to 10X magnification. If not, inform the staff and change it.

2. **Detector Settings**:
   - Detectors: HYDS & HYDX.
     - HYDS: Efficient for blue to yellow spectrum.
     - HYDX: Efficient for yellow to red spectrum.
   - Use the fluorophore panel to assign fluorophores to the appropriate detectors by dragging them from the search results.

3. **Turning On the White Light Laser (WLL)**:
   - When prompted, click "Yes" to turn on the WLL.
   - Ensure no emission spectrum overlap to avoid crosstalk.

4. **Default Parameters**:
   - Lasers: 5%
   - Detectors: 10%
   - Adjust settings as needed based on your experimental requirements.

5. **Image Acquisition Settings**:
   - Avoid taking too many or too few pixels to ensure manageable image sizes and useful resolution for analysis.
   - Use the "Projects" tab to properly name your files, including dates, magnification, and fluorophores used.
   - Save images to the image analysis server: `Z:/project/your_lab_folder`.

## Shutting Down the System

1. **Save and Close Files**:
   - Save all your files.
   - Right-click on the project line and select "Close All."
   - Reset acquisition parameters to default.
   - Delete detector settings by clicking the "X" or trash button.

2. **Clean and Remove Sample**:
   - Change magnification to 10X after cleaning immersion objectives.
   - Remove your sample and clean the microscope room.

3. **Close Software and Log Off**:
   - Close the software (this may take up to 2 minutes).
   - Log off from the booking system.

4. **Turn Off the Controller**:
   - Switch off the key.
   - Turn off the laser switch.
   - Turn off the power switch.

Following these instructions will help ensure proper use and maintenance of the Stellaris confocal microscope, as well as facilitate smooth transitions between users.
