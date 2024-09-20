import React from 'react';
import * as RadixSwitch from '@radix-ui/react-switch';

const Switch = React.forwardRef(({ checked, onCheckedChange, disabled }, ref) => (
  <RadixSwitch.Root
    ref={ref}
    checked={checked}
    onCheckedChange={onCheckedChange}
    disabled={disabled}
    className={`relative inline-flex items-center h-6 w-11 rounded-full transition-colors duration-200 ease-in-out ${checked ? 'bg-green-500' : 'bg-gray-400'}`}
  >
    <span
      className={`inline-block w-5 h-5 transform bg-white rounded-full transition-transform duration-200 ease-in-out ${checked ? 'translate-x-5' : 'translate-x-0'}`}
    />
  </RadixSwitch.Root>
));

Switch.displayName = 'Switch';

export { Switch };