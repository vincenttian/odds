import React, { useState } from 'react';
import { SafeAreaView, Text, TextInput, View } from 'react-native';
import styled from 'styled-components/native';
import { TouchableOpacity } from 'react-native-gesture-handler';

// Styled Components
const Container = styled(SafeAreaView)`
  flex: 1;
  justify-content: center;
  align-items: center;
  background-color: #000;
`;

const Title = styled(Text)`
  font-size: 24px;
  color: #fff;
  margin-bottom: 20px;
  font-weight: bold;
`;

const InputContainer = styled(View)`
  width: 80%;
  margin-top: 20px;
  margin-bottom: 20px;
`;

const PhoneInput = styled(TextInput).attrs({
  placeholderTextColor: '#888',
  keyboardType: 'phone-pad',
})`
  width: 100%;
  padding: 15px;
  border: 1px solid #888;
  border-radius: 10px;
  color: #fff;
  font-size: 18px;
  text-align: center;
  background-color: #333;
`;

const CodeInput = styled(TextInput).attrs({
  placeholderTextColor: '#888',
  keyboardType: 'numeric',
})`
  width: 100%;
  padding: 15px;
  border: 1px solid #888;
  border-radius: 10px;
  color: #fff;
  font-size: 18px;
  text-align: center;
  background-color: #333;
`;

const NextButton = styled(TouchableOpacity)<{ active: boolean }>`
  width: 80%;
  padding: 15px;
  background-color: ${({ active }) => (active ? '#FF4500' : '#555')};
  border-radius: 30px;
  align-items: center;
  justify-content: center;
  margin-top: 20px;
`;

const NextButtonText = styled(Text)`
  color: #fff;
  font-size: 18px;
  font-weight: bold;
`;

const FooterText = styled(Text)`
  color: #aaa;
  font-size: 12px;
  margin-top: 30px;
  text-align: center;
`;

const PhoneNumberScreen = ({ onComplete = () => {} }) => {
  const [phoneNumber, setPhoneNumber] = useState<string>('');
  const [verificationCode, setVerificationCode] = useState<string>('');
  const [isCodeSent, setIsCodeSent] = useState<boolean>(false);

  const isPhoneNumberValid = /^[0-9]{10,15}$/.test(phoneNumber);
  const isVerificationCodeValid = /^[0-9]{6}$/.test(verificationCode);

  const handleNextPress = () => {
    if (isPhoneNumberValid) {
      setIsCodeSent(true);
      // Logic to send verification code goes here
    }
  };

  const handleVerifyPress = () => {
    if (isVerificationCodeValid) {
      onComplete();
      // Add your logic to proceed to the next step
    }
  };

  return (
    <Container>
      <Title>
        {isCodeSent ? 'Enter your verification code' : 'Enter your phone number'}
      </Title>

      <InputContainer>
        {isCodeSent ? (
          <CodeInput
            placeholder="Enter verification code"
            value={verificationCode}
            onChangeText={setVerificationCode}
          />
        ) : (
          <PhoneInput
            placeholder="Enter phone number"
            value={phoneNumber}
            onChangeText={setPhoneNumber}
          />
        )}
      </InputContainer>

      <NextButton
        active={isCodeSent ? isVerificationCodeValid : isPhoneNumberValid}
        onPress={isCodeSent ? handleVerifyPress : handleNextPress}
        disabled={isCodeSent ? !isVerificationCodeValid : !isPhoneNumberValid}
      >
        <NextButtonText>
          {isCodeSent ? 'Verify' : 'Next'}
        </NextButtonText>
      </NextButton>

      <FooterText>
        {/* Footer Text can be included here */}
      </FooterText>
    </Container>
  );
};

export default PhoneNumberScreen;
