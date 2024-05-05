import React from 'react';
import { STS } from 'aws-sdk';
import axios from 'axios';

class App extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      error: '',
      sessionTime: 24 * 60 * 60
    };
    this.craeteUrl = this.craeteUrl.bind(this);
  }

  componentDidMount() {
    this.craeteUrl();
  }

  craeteUrl() {
    try {
      const sts = new STS({
        accessKeyId: import.meta.env.VITE_AWS_ACCESS_KEY,
        secretAccessKey: import.meta.env.VITE_AWS_SECRET_KEY,
        region: import.meta.env.VITE_AWS_REGION
      });

      // const params = {
      //   RoleArn: import.meta.env.VITE_AWS_IAM_ROLE_ARN,
      //   RoleSessionName: 'tuimac',
      //   DurationSeconds: 60 * 60 * 24,
      // };

      const params = {
        PolicyArns: [{ arn: 'arn:aws:iam::aws:policy/AdministratorAccess' }],
        Name: 'tuimac',
        DurationSeconds: this.state.sessionTime,
      };

      sts.getFederationToken(params, (err, data) => {
        if (err) {
          this.setState({ error: err.toString() });
          return;
        }
        console.log(data);
        const { AccessKeyId, SecretAccessKey, SessionToken } = data.Credentials;
        const signinUrl = `https://signin.aws.amazon.com/federation?Action=getSigninToken&SessionDuration=${this.state.sessionTime.toString()}&Session=${encodeURIComponent(SessionToken)}`;
        // axios.post(signinUrl).then((response) => {
        //   console.log(response);
        // }).catch((error) => {
        //   throw error;
        // });
        window.location.href = signinUrl;
      });
    } catch(e) {
      this.setState({ error: e.toString() });
    }
  }

  render() {
    return (
      <>
        <div>
          <p>{ this.state.error }</p>
        </div>
      </>
    );
  }
}

export default App;