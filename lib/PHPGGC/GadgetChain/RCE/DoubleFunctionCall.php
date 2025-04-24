<?php

namespace PHPGGC\GadgetChain\RCE;

/**
 * Class FunctionCall
 * Executes a PHP function with one argument.
 * @package PHPGGC\GadgetChain\RCE
 */
abstract class DoubleFunctionCall extends \PHPGGC\GadgetChain\RCE
{
    public static $type_description = 'RCE: Function Call Two Parameters';

    public static $parameters = [
        'function',
        'parameter1',
        'parameter2',
    ];

    public function test_setup()
    {
        $command = $this->_test_build_command();
        return [
            'function' => 'system',
            'parameter1' =>
                $command
        ];
    }

}
