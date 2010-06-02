<?xml version="1.0" encoding="UTF-8"?>

<!--
 Hive Colony Framework
 Copyright (C) 2008 Hive Solutions Lda.

 This file is part of Hive Colony Framework.

 Hive Colony Framework is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 Hive Colony Framework is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with Hive Colony Framework. If not, see <http://www.gnu.org/licenses/>.
-->

<!--
 __author__    = Jo�o Magalh�es <joamag@hive.pt>
 __version__   = 1.0.0
 __revision__  = $LastChangedRevision: 72 $
 __date__      = $LastChangedDate: 2008-10-21 23:29:54 +0100 (Tue, 21 Oct 2008) $
 __copyright__ = Copyright (c) 2008 Hive Solutions Lda.
 __license__   = GNU General Public License (GPL), Version 3
-->

<build_automation xmlns="http://www.hive.pt"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.hive.pt xsd/baf.xsd">
    <artifact>
        <id>${out value=build_automation.id /}</id>
        <version>${out value=build_automation.version /}</version>
        <type>colony</type>
        <name>${out value=build_automation.name /}</name>
        <description>${out value=build_automation.name /}</description>
        <url>http://www.hive.pt</url>
    </artifact>
    <build>
        <default_stage>build</default_stage>
        <plugins>
            <plugin>
                <id>pt.hive.colony.plugins.build.automation.extensions.packing</id>
                <version>1.0.0</version>
                <stage>build</stage>
                <configuration>
                    <specification_file>$base{plugin_directory}/${out value=build_automation.packing_file /}</specification_file>
                </configuration>
            </plugin>
        </plugins>
    </build>
</build_automation>
