import React, { useState } from "react";

export const STEPS = {
    COMMUNITY: "community",
    NAME: "name",
    CONTACTS: "contacts",
};

const NewUserOnboarding = () => {
    const getNuxSteps = () => [
        STEPS.NAME,
        STEPS.CONTACTS,
        STEPS.COMMUNITY,
    ];

    const [currentStep, setCurrentStep] = useState(0);

    const nuxSteps = getNuxSteps();
    const currentStepValue = currentStep >= nuxSteps.length ? nuxSteps[nuxSteps.length - 1] : nuxSteps[currentStep];

    const goToPreviousStep = () => setCurrentStep(Math.max(currentStep - 1, 0));
    const goToNextStep = () => setCurrentStep(Math.min(currentStep + 1, nuxSteps.length));

    const getStepComponent = () => {
        switch (currentStepValue) {
            case STEPS.COMMUNITY:
                return null;
            case STEPS.NAME:
                return null;
            case STEPS.CONTACTS:
                return null;
        }
    };

    return getStepComponent();
};