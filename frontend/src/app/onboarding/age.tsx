import React, { useState } from 'react';
import { SafeAreaView, Text, View } from 'react-native';
import styled from 'styled-components/native';
import RNPickerSelect from 'react-native-picker-select'; // For the scrollable picker
import { TouchableOpacity } from 'react-native-gesture-handler';

// Styled Components
const Container = styled(SafeAreaView)`
  flex: 1;
  background-color: #000;
  align-items: center;
  justify-content: center;
`;

const Logo = styled.Image`
  width: 120px;
  height: 60px;
  margin-top: 50px;
`;

const AgePickerContainer = styled(View)`
  width: 80%;
  height: 150px;
  justify-content: center;
  margin-top: 30px;
`;

const GetStartedButton = styled(TouchableOpacity)<{ active: boolean }>`
  width: 80%;
  padding: 15px;
  background-color: ${({ active }) => (active ? '#FF4500' : '#555')};
  border-radius: 30px;
  align-items: center;
  justify-content: center;
  margin-top: 30px;
`;

const GetStartedText = styled(Text)`
  color: #fff;
  font-size: 18px;
  font-weight: bold;
`;

const FooterText = styled(Text)`
  color: #aaa;
  font-size: 12px;
  margin-top: 20px;
  text-align: center;
`;

const pickerSelectStyles = {
  inputIOS: {
    fontSize: 18,
    padding: 10,
    backgroundColor: '#333',
    color: '#fff',
    textAlign: 'center',
  },
  inputAndroid: {
    fontSize: 18,
    padding: 10,
    backgroundColor: '#333',
    color: '#fff',
    textAlign: 'center',
  },
};

// Main Component
const AgeSelectionScreen = ({ onComplete = () => {} }) => {

  const [age, setAge] = useState<number | undefined>(undefined);

  const ageOptions = Array.from({ length: 90 }, (_, i) => ({
    label: `${i + 12}`,
    value: i + 12,
  }));

  return (
    <Container>
      {/* Logo at the Top */}
      <Logo source={require('src/assets/images/splash.png')} />

      {/* Scrollable Age Picker */}
      <AgePickerContainer>
        <RNPickerSelect
          onValueChange={(value) => setAge(value)}
          items={ageOptions}
          placeholder={{ label: 'Select your age', value: undefined }}
          value={age}
          style={pickerSelectStyles}
        />
      </AgePickerContainer>

      {/* Get Started Button */}
      <GetStartedButton active={!!age} onPress={() => {
            console.log('Age selected:', age)
            onComplete();
        }}>
        <GetStartedText>Get Started</GetStartedText>
      </GetStartedButton>

      {/* Footer */}
      <FooterText>By entering your age, you agree to our Terms and Privacy Policy.</FooterText>
    </Container>
  );
};

export default AgeSelectionScreen;
