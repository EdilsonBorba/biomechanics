Introduction

This project aims to facilitate the biomechanical analysis of data extracted from OpenCap for walking and running, and eventually for other kinematic data. OpenCap is a widely used tool for capturing movement and collecting biomechanical data. With this project, we aim to create tools and resources that simplify the processing and analysis of this data, allowing for a more detailed and effective understanding of movement patterns during walking and running.

The toolkit will include functionalities for pre-processing data, identifying biomechanical events (such as foot contacts), calculating relevant biomechanical parameters (such as speed, cadence and joint angles), visualizing results and possibly integrating with other libraries and platforms for more advanced analysis.

In addition, the project will focus on comprehensive documentation, with tutorials, usage examples and reference guides to help users use the tools effectively and comprehensively. We are committed to providing an accessible and intuitive solution for biomechanical analysis, thus contributing to the advancement of research and practice in this area.

Requirements

Python 3.x
Libraries: pandas, matplotlib, numpy, scipy, ipywidgets, openpyxl

Notes

Make sure that the correct file paths are provided to OpenCap or by OpenSim.
Adjust filtering parameters (e.g., cutoff frequency, order) as needed for specific datasets.
Additional data processing or analysis steps can be added as per requirements.

References

Uhlrich SD, Falisse A, Kidziński Ł, Muccini J, Ko M, et al. (2023) OpenCap: Human movement dynamics from smartphone videos. PLOS Computational Biology 19(10): e1011462. https://doi.org/10.1371/journal.pcbi.1011462
Seth, A., Hicks, J. L., Uchida, T. K., Habib, A., Dembia, C. L., Dunne, J. J., … Delp, S. L. (2018). OpenSim: Simulating musculoskeletal dynamics and neuromuscular control to study human and animal movement. PLoS Computational Biology, 14(7), 1–20.
Zeni Jr, J., Richards, J., & Higginson, J. (2008). Two simple methods for determining gait events during treadmill and overground walking using kinematic data. Gait & posture, 27(4), 710-714.
