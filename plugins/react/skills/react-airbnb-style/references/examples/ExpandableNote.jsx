/* Airbnb React/JSX: [airbnb-react-jsx:38] constructor-bound handlers;
   [airbnb-react-jsx:39] no arrow fields; [airbnb-react-jsx:42] class ordering.
   Maintenance example for an existing class; new stateful UI may use Hooks. */
import React from 'react';

export default class ExpandableNote extends React.Component {
  constructor(props) {
    super(props);
    this.state = { isExpanded: false };
    this.handleToggle = this.handleToggle.bind(this);
  }

  handleToggle() {
    this.setState(({ isExpanded }) => ({ isExpanded: !isExpanded }));
  }

  render() {
    const { isExpanded } = this.state;

    return (
      <section>
        <button
          type="button"
          aria-expanded={isExpanded}
          onClick={this.handleToggle}
        >
          {isExpanded ? 'Hide note' : 'Show note'}
        </button>
        {isExpanded && <p>This note stays local to the component.</p>}
      </section>
    );
  }
}
