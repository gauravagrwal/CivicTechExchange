// @flow

import React from 'react';
import CurrentUser from "../utils/CurrentUser.js";

type Props = {|

|};

type State = {|
|}

class SignedUpController extends React.Component<Props, State> {
  constructor(): void {
    super();
  }

  render(): React$Node {
    // TODO: Give indication that email has been sent
    return (
      <div className="LogInController-root">
        <div className="LogInController-logo">
          <img src="/static/images/projectPlaceholder.png"/>
        </div>
        <div className="LogInController-greeting">
          <h3>Check your email</h3>
          <p>We've sent a message to {CurrentUser.email()}</p>
          <p>with a link to verify your account.</p>
          <br></br>
          <p>Didn't get an email?</p>
          <a href="/verify_user">Resend verification email</a>
        </div>
      </div>
    );
  }
}

export default SignedUpController;
