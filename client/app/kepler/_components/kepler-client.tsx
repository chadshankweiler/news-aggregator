"use client";

import React from "react";
import { connect } from "react-redux";
import { AutoSizer } from "react-virtualized";
import { KeplerGl } from "@kepler.gl/components";
import { addDataToMap } from "@kepler.gl/actions";
import type { RootState, AppDispatch } from "@/lib/store";

interface OwnProps {
    mapboxApiAccessToken?: string;
    id?: string;
    initialData?: any;
    initialConfig?: any;
}

interface StateProps {
    keplerGl: any;
}

interface DispatchProps {
    addDataToMap: typeof addDataToMap;
}

type KeplerGlClientProps = OwnProps & StateProps & DispatchProps;

const mapStateToProps = (state: RootState): StateProps => ({
    keplerGl: state.keplerGl,
});

const mapDispatchToProps = (dispatch: AppDispatch): DispatchProps => ({
    addDataToMap: (data: any) => dispatch(addDataToMap(data)),
});

function KeplerGlClient(props: KeplerGlClientProps) {
    React.useEffect(() => {
        if (
            props.initialData &&
            props.keplerGl &&
            !props.keplerGl[props.id || "map"]?.mapState
        ) {
            props.addDataToMap({
                datasets: props.initialData,
                config: props.initialConfig,
                options: { mapsetId: props.id },
            });
        }
    }, [
        props.initialData,
        props.initialConfig,
        props.addDataToMap,
        props.keplerGl,
        props.id,
    ]);

    return (
        <div style={{ position: "absolute", width: "100%", height: "100%" }}>
            <AutoSizer>
                {({ height, width }: { height: number; width: number }) => (
                    <KeplerGl
                        mapboxApiAccessToken={props.mapboxApiAccessToken}
                        id={props.id || "map"}
                        width={width}
                        height={height}
                    />
                )}
            </AutoSizer>
        </div>
    );
}

const ConnectedKeplerGlClient = connect(
    mapStateToProps,
    mapDispatchToProps
)(KeplerGlClient);

export default ConnectedKeplerGlClient;
